# Email Client Quirks — why each rule exists

## Outlook desktop (Windows) — renders with Microsoft Word's engine

- Ignores `max-width` → wrap the 600px container in a `<!--[if mso]>` ghost table with a fixed `width="600"`.
- Ignores web/system font stacks and falls back to **Times New Roman** → the `[if mso]` style block forces Arial on `body, table, td, p, a, span, div`.
- No `border-radius`, no `box-shadow`, weak `padding` on `<a>` → buttons need the **VML `v:roundrect`** variant with `<w:anchorlock/>` and a `<center>` label; the regular anchor carries `mso-hide:all` so Outlook never shows both.
- Adds mystery spacing around tables → reset with `mso-table-lspace:0pt; mso-table-rspace:0pt; border-collapse:collapse`.
- PNG handling and DPI scaling on high-DPI Windows → `<o:OfficeDocumentSettings>` with `<o:AllowPNG/>` and `<o:PixelsPerInch>96</o:PixelsPerInch>`.
- Honors `dir="rtl"` on tables — safe to use for the flush-right trick (cells reset `dir="ltr"`).
- Image `width`/`height` must be HTML attributes, not only CSS.

## Gmail (web + apps)

- May strip or partially ignore `<head><style>` (especially with `@import`, long blocks, or in forwarded/clipped mail) → **all layout styles inline**; the style block is expendable reset + media queries only.
- **Clips messages over ~102 KB** of HTML ("[Message clipped] View entire message") — keep the file small; the clipped view hides the unsubscribe link, which hurts deliverability.
- Auto-colors detected links → `u + #body a { color:inherit }` fix (body needs `id="body"`).
- Caches images through its proxy aggressively → cache-buster query param (`?v=N`) on every image URL, bumped when the asset changes.

## Apple Mail / iOS

- Auto-detects dates, addresses, phone numbers and paints them blue → `a[x-apple-data-detectors]` reset + `format-detection` meta.
- Reformats/zooms narrow layouts → `<meta name="x-apple-disable-message-reformatting" />`.
- Respects media queries fully — the mobile block does the real work here.

## Dark mode (Apple Mail, Outlook apps, Gmail app)

- Clients invert or shift colors unless told otherwise → `color-scheme: light only` + `supported-color-schemes: light only` meta pair keeps brand colors intact. Design a real dark variant only deliberately.

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

- Renderers cannot be trusted from screenshots alone: send **real test mails** (e.g. Brevo test-send) to Outlook desktop, Gmail web, and one phone.
- Expect 2–3 review iterations with a human looking at the actual inbox; log what each iteration changed.
- After changing a hosted image, bump its `?v=` and re-test — otherwise you review a cached asset.
