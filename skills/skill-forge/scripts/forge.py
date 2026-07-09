#!/usr/bin/env python3
"""forge — scaffold, validate, list, package, and dashboard Claude Code skills.

Stdlib-only. Usage:
  forge.py new <name> [--dir DIR] [--description TEXT]
  forge.py validate [PATH ...] [--all] [--json]
  forge.py list [--json]
  forge.py dashboard [--out FILE] [--open]
  forge.py package <PATH> [--out DIR]
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PERSONAL_SKILLS = Path.home() / ".claude" / "skills"
PROJECT_ROOT = Path.cwd()

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Portable core — the exact whitelist enforced by Anthropic's quick_validate.py
SPEC_FIELDS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
# Claude Code extensions — valid there, not portable to other Agent Skills hosts
CC_FIELDS = {
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "disallowed-tools", "model", "effort", "context",
    "agent", "hooks", "paths", "shell", "version",
}
RESERVED_NAME_WORDS = ("anthropic", "claude")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_BODY_LINES = 500
MAX_BODY_WORDS = 5000

FRESH_DAYS = 30
AGING_DAYS = 90

DANGEROUS_PATTERNS = [
    (re.compile(r"rm\s+-[a-z]*rf?[a-z]*\s+[/~]"), "'rm -rf' on / or ~"),
    (re.compile(r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh"), "'curl | sh' remote-execute"),
    (re.compile(r"\bsudo\b"), "'sudo'"),
    (re.compile(r"chmod\s+777"), "'chmod 777'"),
    (re.compile(r"base64\s+(-d|--decode)[^\n|]*\|\s*(ba|z)?sh"), "base64-decoded shell execution"),
]

PACKAGE_EXCLUDES = {"__pycache__", "node_modules", ".DS_Store", ".git"}


# ---------------------------------------------------------------- discovery

def find_skill_dirs(extra_paths=None):
    """Yield (source, skill_dir) for personal + project skills."""
    seen = set()
    roots = [("personal", PERSONAL_SKILLS)]
    for candidate in (PROJECT_ROOT / "skills", PROJECT_ROOT / ".claude" / "skills"):
        roots.append(("project", candidate))
    out = []
    for source, root in roots:
        if not root.is_dir():
            continue
        for entry in sorted(root.iterdir()):
            if entry.is_dir() and (entry / "SKILL.md").is_file():
                real = entry.resolve()
                if real not in seen:
                    seen.add(real)
                    out.append((source, entry))
    for p in extra_paths or []:
        p = Path(p)
        if (p / "SKILL.md").is_file() and p.resolve() not in seen:
            seen.add(p.resolve())
            out.append(("path", p))
    return out


# ---------------------------------------------------------- frontmatter I/O

def split_frontmatter(text):
    """Return (frontmatter_lines or None, body). Tolerant of missing block."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, text  # unterminated block


def parse_frontmatter(fm_lines):
    """Minimal YAML-subset parser: `key: value`, quoted strings, folded
    continuations, and one level of nested maps (e.g. metadata:)."""
    data, order = {}, []
    current_key = None
    for raw in fm_lines:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and indent == 0:
            key, value = m.group(1), m.group(2)
            order.append(key)
            current_key = key
            data[key] = _unquote(value)
        elif current_key is not None:
            # continuation or nested content — append textually
            prev = data.get(current_key) or ""
            data[current_key] = (prev + " " + line).strip()
    return data, order


def _unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value in (">", "|", ">-", "|-"):
        return ""
    return value


# ------------------------------------------------------------------ checks

def last_updated(path):
    """Last git commit touching path, else newest mtime in the dir."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            capture_output=True, text=True, cwd=str(path), timeout=5,
        )
        if out.returncode == 0 and out.stdout.strip():
            return datetime.fromisoformat(out.stdout.strip())
    except Exception:
        pass
    newest = 0
    for p in path.rglob("*"):
        if p.is_file():
            newest = max(newest, p.stat().st_mtime)
    if not newest:
        newest = path.stat().st_mtime
    return datetime.fromtimestamp(newest, tz=timezone.utc)


def freshness(updated):
    age = (datetime.now(timezone.utc) - updated).days
    if age <= FRESH_DAYS:
        return "fresh", age
    if age <= AGING_DAYS:
        return "aging", age
    return "stale", age


def validate_skill(skill_dir):
    """Return report dict with errors[], warnings[], info{}."""
    skill_dir = Path(skill_dir)
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    report = {
        "dir": str(skill_dir),
        "name": skill_dir.name,
        "errors": errors,
        "warnings": warnings,
        "meta": {},
    }
    if not skill_md.is_file():
        errors.append("SKILL.md is missing")
        return report

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm_lines, body = split_frontmatter(text)

    if fm_lines is None:
        errors.append("no YAML frontmatter block (--- ... ---) at top of SKILL.md")
        meta = {}
    else:
        meta, order = parse_frontmatter(fm_lines)
        report["meta"] = meta
        for key in order:
            if key in SPEC_FIELDS:
                continue
            if key in CC_FIELDS:
                warnings.append(
                    f"'{key}' is a Claude Code extension field — fine here, "
                    "not portable to other Agent Skills hosts"
                )
            else:
                warnings.append(f"unknown frontmatter field '{key}'")

        name = meta.get("name", "")
        if not name:
            errors.append("frontmatter is missing 'name'")
        else:
            if len(name) > MAX_NAME:
                errors.append(f"name is {len(name)} chars (max {MAX_NAME})")
            if not NAME_RE.match(name):
                errors.append("name must be lowercase letters/digits/hyphens "
                              "(no leading/trailing/double hyphens)")
            if any(w in name.split("-") for w in RESERVED_NAME_WORDS):
                warnings.append("name contains a reserved word ('anthropic'/'claude')")
            if name != skill_dir.name:
                warnings.append(
                    f"name '{name}' does not match directory '{skill_dir.name}' "
                    "— the Agent Skills spec requires them to match"
                )

        desc = meta.get("description", "")
        if not desc:
            errors.append("frontmatter is missing 'description'")
        else:
            if len(desc) > MAX_DESCRIPTION:
                errors.append(
                    f"description is {len(desc)} chars (max {MAX_DESCRIPTION})"
                )
            if "<" in desc or ">" in desc:
                errors.append("description contains angle brackets — the spec rejects XML tags")
            if len(desc) < 20:
                warnings.append("description is very short — add what it does AND when to use it")
            low = desc.lower()
            if not any(t in low for t in ("use when", "use this", "use for", "use whenever", "trigger", "use it when")):
                warnings.append("description has no 'when to use' cue (e.g. 'Use when ...') — hurts auto-triggering")
            if re.search(r"\b(I|me|my)\b", desc):
                warnings.append("description uses first person — write in third person")

        compat = meta.get("compatibility", "")
        if compat and len(compat) > MAX_COMPATIBILITY:
            errors.append(f"compatibility is {len(compat)} chars (max {MAX_COMPATIBILITY})")

    body_lines = body.count("\n") + 1
    body_words = len(body.split())
    report["lines"] = body_lines
    report["words"] = body_words
    if body_lines > MAX_BODY_LINES:
        warnings.append(f"body is {body_lines} lines (aim <{MAX_BODY_LINES}) — move detail to references/")
    if body_words > MAX_BODY_WORDS:
        warnings.append(f"body is {body_words} words (aim <{MAX_BODY_WORDS}) — move detail to references/")

    for marker in ("TODO:", "FIXME:", "[TODO", "[PLACEHOLDER]"):
        if marker in body:
            warnings.append(f"body still contains '{marker}'")

    # safety scan of bundled scripts (real-world skill malware exists)
    for script in skill_dir.glob("scripts/**/*"):
        if script.suffix not in (".sh", ".bash", ".py", ".js", ".ts", ".zsh"):
            continue
        try:
            lines = script.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            stripped = line.strip()
            # skip comments and pattern/string definitions (a scanner scanning itself)
            if stripped.startswith(("#", "//", "*")) or "re.compile" in stripped:
                continue
            for pat, label in DANGEROUS_PATTERNS:
                if pat.search(line):
                    warnings.append(
                        f"{script.relative_to(skill_dir)}: contains {label} — review before trusting"
                    )
                    break

    # relative links / file references that don't exist
    for target in re.findall(r"\]\(([^)#]+?)\)|`((?:references|scripts|assets)/[^`\s]+)`", body):
        rel = (target[0] or target[1]).strip()
        if not rel or rel.startswith(("http://", "https://", "mailto:", "/")):
            continue
        if not (skill_dir / rel).exists():
            warnings.append(f"references missing file: {rel}")

    updated = last_updated(skill_dir)
    state, age = freshness(updated)
    report["updated"] = updated.isoformat()
    report["age_days"] = age
    report["freshness"] = state
    report["files"] = sum(1 for p in skill_dir.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    report["status"] = "error" if errors else ("warning" if warnings else "ok")
    return report


# --------------------------------------------------------------- scaffold

SKILL_TEMPLATE = """---
name: {name}
description: "{description}"
---

# {title}

One-paragraph summary of what this skill does and the result it produces.

## When to use

- Bullet the concrete situations that should trigger this skill.

## Workflow

1. Step one.
2. Step two.
3. Step three.

## References

- `references/` — deep-dive docs loaded only when needed.
- `scripts/` — executable helpers (run them, don't paraphrase them).
"""


def cmd_new(args):
    name = args.name
    if not NAME_RE.match(name):
        sys.exit(f"error: '{name}' — skill names must be lowercase letters/digits/hyphens")
    if len(name) > MAX_NAME:
        sys.exit(f"error: name exceeds {MAX_NAME} chars")
    base = Path(args.dir) if args.dir else (PROJECT_ROOT / "skills")
    skill_dir = base / name
    if skill_dir.exists():
        sys.exit(f"error: {skill_dir} already exists")
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "scripts").mkdir()
    description = args.description or (
        f"[PLACEHOLDER] What {name} does. Use when <trigger situations>."
    )
    title = name.replace("-", " ").title()
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, description=description, title=title),
        encoding="utf-8",
    )
    (skill_dir / "references" / ".gitkeep").touch()
    (skill_dir / "scripts" / ".gitkeep").touch()
    (skill_dir / "evals").mkdir()
    (skill_dir / "evals" / "evals.json").write_text(json.dumps({
        "queries": [
            {"query": f"[PLACEHOLDER] a user request that SHOULD trigger {name}", "should_trigger": True},
            {"query": "[PLACEHOLDER] a nearby request that should NOT trigger it", "should_trigger": False},
        ]
    }, indent=2) + "\n", encoding="utf-8")
    print(f"created {skill_dir}")
    print("next: edit SKILL.md, then run: forge.py validate " + str(skill_dir))


# ---------------------------------------------------------------- validate

def collect_reports(paths, all_skills):
    if paths:
        dirs = [("path", Path(p)) for p in paths]
    else:
        dirs = find_skill_dirs()
    reports = [dict(validate_skill(d), source=src) for src, d in dirs]
    # cross-skill name collisions (a personal skill silently shadows a project one)
    by_name = {}
    for r in reports:
        by_name.setdefault(r["meta"].get("name") or r["name"], []).append(r)
    for name, group in by_name.items():
        if len(group) > 1:
            for r in group:
                others = ", ".join(g["dir"] for g in group if g is not r)
                r["warnings"].append(f"name '{name}' collides with skill at {others}")
                if r["status"] == "ok":
                    r["status"] = "warning"
    return reports


def cmd_validate(args):
    reports = collect_reports(args.paths, args.all)
    if args.json:
        print(json.dumps(reports, indent=2))
    else:
        for r in reports:
            icon = {"ok": "✓", "warning": "⚠", "error": "✗"}[r["status"]]
            print(f"{icon} {r['name']}  ({r['dir']})")
            for e in r["errors"]:
                print(f"    ERROR   {e}")
            for w in r["warnings"]:
                print(f"    warning {w}")
        errs = sum(len(r["errors"]) for r in reports)
        warns = sum(len(r["warnings"]) for r in reports)
        print(f"\n{len(reports)} skill(s): {errs} error(s), {warns} warning(s)")
    if any(r["errors"] for r in reports):
        sys.exit(1)


def cmd_list(args):
    reports = collect_reports([], True)
    if args.json:
        print(json.dumps(reports, indent=2))
        return
    width = max((len(r["name"]) for r in reports), default=4) + 2
    print(f"{'NAME':<{width}}{'SOURCE':<10}{'STATUS':<9}{'WORDS':<7}{'AGE':<6}DESCRIPTION")
    for r in reports:
        desc = (r["meta"].get("description") or "—")[:60]
        print(f"{r['name']:<{width}}{r['source']:<10}{r['status']:<9}"
              f"{r.get('words', 0):<7}{r.get('age_days', '?'):<6}{desc}")


# ----------------------------------------------------------------- package

def cmd_package(args):
    skill_dir = Path(args.path)
    report = validate_skill(skill_dir)
    if report["errors"]:
        for e in report["errors"]:
            print(f"ERROR {e}", file=sys.stderr)
        sys.exit("refusing to package a skill with validation errors")
    out_dir = Path(args.out or "dist")
    out_dir.mkdir(parents=True, exist_ok=True)
    # official skill-creator convention: <name>.skill zip, evals/ excluded
    zip_path = out_dir / f"{skill_dir.name}.skill"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(skill_dir.rglob("*")):
            rel = p.relative_to(skill_dir)
            if (not p.is_file() or p.suffix == ".pyc"
                    or PACKAGE_EXCLUDES.intersection(p.parts)
                    or rel.parts[0] == "evals"):
                continue
            zf.write(p, Path(skill_dir.name) / rel)
    print(f"packaged → {zip_path}")


# --------------------------------------------------------------- dashboard

def cmd_dashboard(args):
    reports = collect_reports([], True)
    out = Path(args.out or PROJECT_ROOT / "docs" / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    template = Path(__file__).parent / "dashboard_template.html"
    html_text = render_dashboard(reports, template)
    out.write_text(html_text, encoding="utf-8")
    print(f"dashboard → {out}  ({len(reports)} skills)")
    if args.open:
        subprocess.run(["open", str(out)])


def render_dashboard(reports, template_path):
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    payload = json.dumps([
        {
            "name": r["name"],
            "source": r["source"],
            "status": r["status"],
            "errors": r["errors"],
            "warnings": r["warnings"],
            "description": r["meta"].get("description", ""),
            "words": r.get("words", 0),
            "lines": r.get("lines", 0),
            "files": r.get("files", 0),
            "age_days": r.get("age_days"),
            "freshness": r.get("freshness", "unknown"),
            "updated": r.get("updated", ""),
            "dir": r["dir"],
        }
        for r in reports
    ], indent=None)
    template = template_path.read_text(encoding="utf-8")
    return (template
            .replace("/*__DATA__*/[]", payload)
            .replace("__GENERATED__", html.escape(generated)))


# --------------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(prog="forge.py", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="scaffold a new skill")
    p.add_argument("name")
    p.add_argument("--dir", help="parent directory (default ./skills)")
    p.add_argument("--description")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("validate", help="lint skills")
    p.add_argument("paths", nargs="*")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("list", help="list all discovered skills")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("dashboard", help="generate the HTML dashboard")
    p.add_argument("--out")
    p.add_argument("--open", action="store_true")
    p.set_defaults(fn=cmd_dashboard)

    p = sub.add_parser("package", help="zip a skill for distribution")
    p.add_argument("path")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_package)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
