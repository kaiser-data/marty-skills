# Email Client Quirks — why each rule exists

## Outlook desktop (Windows) — CLASSIC Outlook renders with Microsoft Word's engine

**Scope note:** everything below applies to *classic* Outlook (Word engine, supported until ~2029). The **new Outlook for Windows is Chromium-based** (WebView2) and renders like Outlook.com — no Word quirks, no VML. The `[if mso]` blocks are still required for the classic audience, but that share shrinks every year.

- Ignores `max-width` → wrap the 600px container in a `<!--[if mso]>` ghost table with a fixed `width="600"`.
- Ignores web/system font stacks and falls back to **Times New Roman** → the `[if mso]` style block forces Arial on `body, table, td, p, a, span, div`.
- No `border-radius`, no `box-shadow`, weak `padding` on `<a>` → buttons need the **VML `v:roundrect`** variant with `<w:anchorlock/>` and a `<center>` label; the regular anchor carries `mso-hide:all` so Outlook never shows both.
- Adds mystery spacing around tables → reset with `mso-table-lspace:0pt; mso-table-rspace:0pt; border-collapse:collapse`.
- PNG handling and DPI scaling on high-DPI Windows → `<o:OfficeDocumentSettings>` with `<o:AllowPNG/>` and `<o:PixelsPerInch>96</o:PixelsPerInch>`.
- Honors `dir="rtl"` on tables — safe to use for the flush-right trick (cells reset `dir="ltr"`).
- Image `width`/`height` must be HTML attributes, not only CSS.
- **Background image needed anyway?** Don't rule it out — use the VML recipe: `<v:rect fill="true" stroke="false">` + `<v:fill type="frame" src="...">` inside `[if mso]`, regular CSS `background` for everyone else (Cerberus documents the full pattern). Still design for the solid-color fallback.

## Buttons: two bulletproof techniques

1. **VML `v:roundrect` + `mso-hide:all` anchor pair** (the battle-tested default in `skeleton.html`) — pixel-perfect in classic Outlook, but two DOM variants to keep in sync and the VML side is invisible to screen readers.
2. **Single-anchor with MSO padding fake** (`skeleton-hybrid.html`, goodemailcode.com): one `<a>` with `padding` + `mso-padding-alt:0`; classic Outlook gets horizontal padding from `[if mso]` `<i>` elements with `mso-font-width` (≤500%) around the label, vertical padding from `mso-text-raise` (100% on the leading `<i>`, ~50% on the label `<span>`). One node, accessible, no duplicate label. Prefer it for new templates; keep VML where a design demands exact rounded corners in classic Outlook.
- Accessibility either way: never `role="button"` on a link — email has no JS, a fake button just loses link semantics for screen readers.

## Gmail (web + apps)

- May strip or partially ignore `<head><style>` (especially with `@import`, long blocks, or in forwarded/clipped mail) → **all layout styles inline**; the style block is expendable reset + media queries only.
- **Clips messages over ~102 KB** of HTML ("[Message clipped] View entire message"). The limit counts **HTML bytes only** (images don't count). Clipping cuts whatever sits at the bottom — typically the **unsubscribe link and the open-tracking pixel** — so a clipped mail both hurts deliverability and under-reports opens. Target **~80–90 KB**: strip unused CSS/classes and minify before send.
- Auto-colors detected links → `u + #body a { color:inherit }` fix (body needs `id="body"`).
- Caches images through its proxy aggressively → cache-buster query param (`?v=N`) on every image URL, bumped when the asset changes.
- Shows a **download-overlay icon** on images wider than ~300px → add `class="g-img"` to the image plus `img.g-img + div { display:none !important; }` in the style block.
- **Media queries work ONLY for Google accounts.** A Yahoo/work mailbox read *in the Gmail app* (a "non-Google account") gets NO media-query support — the mobile block silently never fires. This is the reason the hybrid skeleton exists: `display:inline-block; width:100%; max-width` reflows without media queries. When using the fixed-width skeleton, know that this audience sees the desktop layout scaled down.

## Apple Mail / iOS

- Auto-detects dates, addresses, phone numbers and paints them blue → `a[x-apple-data-detectors]` reset + `format-detection` meta.
- Reformats/zooms narrow layouts → `<meta name="x-apple-disable-message-reformatting" />`.
- Respects media queries fully — the mobile block does the real work here.

## Dark mode (Apple Mail, Outlook apps, Gmail app)

Three client behaviors: no change / partial invert (light backgrounds darkened, dark text lightened) / **full invert regardless of your wishes** (Gmail app, Outlook mobile).

- The `color-scheme: light only` + `supported-color-schemes` meta pair is a **hint, not a guarantee** — honored by Apple Mail and a few others (~5% weighted support), **ignored by exactly the full-invert clients it targets**. Keep it, but don't rely on it.
- The real defenses are design-side:
  - **Avoid pure `#000`/`#fff`** — forced inversion flips pure colors hard; near-neutrals (`#121212`-ish darks, `#F1F1F1`-ish lights) invert gracefully.
  - **Transparent-PNG logos with built-in padding/outline** so the mark survives on both light and dark backgrounds.
  - Check that brand colors keep ≥4.5:1 contrast after a simulated invert.
- Deliberate dark styling where supported: `@media (prefers-color-scheme: dark)` reaches Apple Mail (Gmail and Yahoo ignore it); `[data-ogsc]` (text) / `[data-ogsb]` (background) attribute selectors re-style content **after** Outlook.com/Outlook-app recoloring.
- Design a real dark variant only deliberately; test in at least one full-invert client (Gmail app) before trusting any mail's dark rendering.

## Mobile media query decisions (user-tested at 320–620px)

- Breakpoint 620px (just above the 600px container).
- Container → `width:100%`; horizontal padding → 22px.
- Big CTAs: `display:inline-block; width:auto; padding:12px 20px; line-height:21px` — the button **hugs its label and stays centered**. Full-width block buttons tested worse; a 2-line wrapped label with the desktop `line-height:50px` produced a huge button.
- Header bar stays on ONE line: logo shrinks (84 → 72px), header button padding tightens (9/18 → 8/14px) so both fit a 320px screen.

## Preheader mechanics

- First element in `<body>`: hidden div (`display:none; max-height:0; mso-hide:all; opacity:0`) with ~90 chars of preview text.
- Follow with repeated `&nbsp;&zwnj;` pairs so clients that show ~110 preview chars don't leak body copy after the preheader.
- Color it the page background color as extra insurance.

## Testing protocol

- Renderers cannot be trusted from screenshots alone: send **real test mails** (every ESP has this — Brevo, CleverReach, Mailchimp, SendGrid) to Outlook desktop, Gmail web, and one phone.
- Expect 2–3 review iterations with a human looking at the actual inbox; log what each iteration changed.
- After changing a hosted image, bump its `?v=` and re-test — otherwise you review a cached asset.

## Testing tools (recommend to the user; verify pricing before subscribing)

Real test sends stay the final gate — these tools reduce iterations, they don't replace the check:

- **Screenshot walls** (render the HTML in dozens of real clients incl. classic Outlook + dark mode): **Testi@** (testi.at, free tier) is the budget pick; **Litmus** (~$99+/mo) and **Email on Acid/Sinch** (~$74+/mo) are the professional references.
- **PutsMail** (putsmail.com, free, by Litmus): paste raw HTML and send it to your own test addresses — test the markup without creating an ESP draft.
- **mail-tester.com** (free): spam/deliverability preflight — 0–10 score for SPF/DKIM/DMARC, spam triggers, HTML weight. Belongs before every campaign (details in the `email-deliverability` skill).
- **Mailtrap** (free tier): sandbox SMTP that catches test sends and reports client CSS-support warnings, spam score, and blacklist status before anything hits a real inbox.
- **Parcel** (parcel.io, free tier): email-specific code editor with live previews — good for iterating on a skeleton.
- **caniemail.com**: per-property client support — check before using any CSS feature not already in the skeletons.
