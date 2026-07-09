---
name: html-email
description: "Draft bulletproof HTML emails that render correctly in the maximum range of email clients (Outlook desktop, Gmail, Apple Mail, AOL/Yahoo, mobile apps). Use when writing or editing email HTML: newsletters, campaign mails, confirmation/welcome mails, email templates, Brevo/Mailchimp/SendGrid campaigns, or when a mail renders broken in Outlook/Gmail or lands in spam."
---

# HTML Email Drafting

Produce campaign-grade HTML email that survives the hostile rendering landscape: Outlook desktop uses Word's engine, Gmail strips `<style>` unpredictably, images are blocked by default, and mobile clients reflow everything. These rules were battle-tested across Outlook, Gmail, Apple Mail, and AOL in real campaign sends (161/162 delivered, user-reviewed over multiple test iterations).

## Non-negotiable ground rules

1. **Tables, not divs.** Layout is nested `<table role="presentation" cellspacing="0" cellpadding="0" border="0">`. One 600px-wide container table (`width="600"` attribute AND `style="width:600px;max-width:600px"`), centered in a full-width background table.
2. **Inline every layout-critical style.** The `<style>` block in `<head>` holds ONLY the reset and mobile media queries — Gmail may strip parts of it, so nothing layout-critical lives there.
3. **XHTML transitional doctype** with VML namespaces on `<html>`: `xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"`.
4. **Solid `bgcolor` everywhere a background matters** — set it as HTML attribute AND inline style. Background images are not bulletproof; a solid-color band with alt-texted image on top degrades gracefully when images are blocked.
5. **HTML entities for all non-ASCII** (`&uuml;`, `&ndash;`, `&euro;`) — survives any charset mangling in transit.
6. **Every `<img>`**: absolute HTTPS URL with a cache-buster (`?v=N`, bump N when the asset changes — clients and proxies cache hard), `width`/`height` attributes, meaningful `alt`, `style="display:block;border:0;height:auto;-ms-interpolation-mode:bicubic"`.
7. **Merge tags stay literal** (`{{ FIRSTNAME }}`, `{{ UNSUBSCRIBE }}`) — map them to the sending system's syntax only at send time; comment which system they target.

## Workflow

1. Pick a skeleton — never hand-roll the head block:
   - `references/skeleton.html` — the **battle-tested default** (fixed 600px + media queries, VML buttons). Proven in real sends.
   - `references/skeleton-hybrid.html` — fluid "spongy" variant that reflows **without media queries** (covers Gmail-app users on non-Google accounts, where media queries never fire). **Not yet proven in real sends** — A/B against the default in test sends before using for a live campaign.
2. Write copy into the body sections; keep paragraph styling on each `<p>` (`margin:0 0 18px 0`, font stack, size, line-height on the containing `<td>`).
3. Buttons: two bulletproof options (details + trade-offs in `references/client-quirks.md`). The proven default is the **VML + anchor pair** (`v:roundrect` for classic Outlook, `mso-hide:all` anchor for the rest — both variants same label and href). The modern alternative is a **single anchor with MSO padding fake** (`mso-padding-alt` + `[if mso]` `<i>`/`mso-font-width`/`mso-text-raise`) — one node, screen-reader friendly. Never `role="button"` on a link.
4. Add the hidden **preheader** div as the first body element — the inbox preview line. Pad it with `&nbsp;&zwnj;` repeats so body text doesn't leak into the preview.
5. Check the mobile media query (`max-width:620px`): container 100%, side padding tightens to 22px, headline shrinks, CTAs become `display:inline-block; width:auto; line-height:21px; padding:12px 20px` — buttons **hug their label, centered**, not full-width; a wrapped 2-line label needs the tight 21px line-height instead of the desktop 50px row. Layout must survive a 320px screen.
6. Footer is mandatory: sender identity/Impressum, why-you-got-this line, `{{ UNSUBSCRIBE }}` link. Missing unsubscribe = spam folder + legal problem.
7. **Verify before sending**: real test sends to Outlook + Gmail + one mobile client minimum; iterate on what the user sees. Renderers cannot be simulated reliably — expect 2–3 test iterations.

## Layout techniques that work everywhere

- **Flush-right element in a bar** (e.g. logo right, button left): put cells in a `dir="rtl"` table with the right-most element FIRST in the DOM, each cell reset to `dir="ltr"`. Outlook honors `dir=rtl`. Percent-width spacer cells (`font-size:0;line-height:0`) control the gap.
- **Ghost table for Outlook**: wrap the 600px container in `<!--[if mso]><table width="600"><tr><td><![endif]-->` … `<!--[if mso]></td></tr></table><![endif]-->` — Outlook ignores `max-width`.
- **Horizontal rule**: a 1px `<td>` with `bgcolor`, `height:1px;line-height:1px;font-size:1px;` containing `&nbsp;` — never `<hr>`.
- **Boxed callout**: nested table with `bgcolor`, 1px border, `border-radius` (progressive enhancement — Outlook shows square corners, acceptable).

## Accessibility (legally required in the EU since June 2025 — EAA)

- Real heading elements (`<h1>`–`<h3>`) for headings, not styled `<p>` — screen readers navigate by them.
- `lang` attribute on `<html>` AND `<body>`.
- `role="presentation"` on every layout table (already in the skeletons); meaningful `alt` on every image.
- Text contrast ≥ 4.5:1 — including after dark-mode inversion (see client-quirks.md).

## Spam-safe markup & size

- Keep image-to-text ratio sane; the mail must make sense with all images blocked (alt text + solid color bands).
- One clear primary CTA URL repeated is fine; many different link domains is a spam signal.
- **Stay under ~90 KB of HTML** (Gmail clips at ~102 KB, HTML bytes only) — clipping hides the unsubscribe link and the tracking pixel. Strip unused CSS/classes before send.
- Dark mode: the `color-scheme: light only` meta pair is a hint honored by few clients, NOT a guarantee — the real defense is color choice (no pure #000/#fff, transparent-PNG logos). Full strategy in `references/client-quirks.md`.

This skill covers only the markup. Delivery diagnosis (spam folder, bounces, sender reputation, campaign checks) is the companion `email-deliverability` skill.

## References

- `references/skeleton.html` — the full proven boilerplate to copy as starting point (head, preheader, header bar, VML buttons, callout box, footer).
- `references/skeleton-hybrid.html` — fluid no-media-query variant (hybrid columns, single-anchor buttons, real headings). Untested in live sends — verify before campaign use.
- `references/client-quirks.md` — per-client gotchas (classic vs new Outlook, Gmail clipping + non-Google-account limits, Apple data detectors, dark-mode strategy, button techniques), line by line.
