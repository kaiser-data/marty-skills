---
name: linkedin-unicode-styling
description: Use when a LinkedIn or social post needs bold, headers, small caps or other Unicode glyph styling — including when a post is near its character limit, when styled headers are being added or restyled, when @-mentions or hashtags stop autocompleting, or when styled text appears literally in a draft file.
---

# LinkedIn Unicode Styling

LinkedIn strips Markdown. The only way to get bold or headers is to swap letters for
Mathematical Alphanumeric glyphs (𝗯𝗼𝗹𝗱) — real Unicode letters that happen to look styled.
They cost double, break tagging, and degrade for screen readers. Style on purpose, or not at all.

## The one rule that prevents the worst bug

**Styled glyphs NEVER go into the source draft.** Write plain Markdown (`**bold**`) or a
style directive; convert at export time.

Glyphs in a source file are invisible damage: grep and diff stop matching, spellcheck dies,
every future agent editing the file has to hand-copy glyphs to stay consistent, and a
restyle means rewriting instead of changing one converter. If you find glyphs in a draft,
convert them back to Markdown — that's a fix, not a refactor.

## Cost: styled characters count double

Astral-plane glyphs (U+1D400 and up) are 2 UTF-16 units each. Most platform counters —
LinkedIn's 3000-char limit included — count units, not visible characters.

**An 11-character bold header costs 22.** Budget before styling, not after.

| Style | Cost/char | Safe? | Looks like |
|---|---|---|---|
| Bold sans, serif, italic, mono | **2×** | yes | 𝗧𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁 |
| Small caps | **1×** | yes | ᴛʜᴇ ʀᴇꜱᴜʟᴛ |
| Fullwidth | **1×** | yes, but wrecks mobile wrapping | Ｔｈｅ |
| Circled, squared | 1–2× | poor screen-reader support | Ⓣⓗⓔ |
| Script, fraktur, double-struck | 2× | **no** — often tofu boxes, unreadable aloud | 𝔗𝔥𝔢 |
| Block/geometric markers (▎ ◆ ━ •) | **1×** | yes | ▎ |

**Small caps are the budget escape hatch:** same visual structure as a bold header at half
the cost. Four bold headers = 78 chars; four small-caps headers = 41.

**Markers are nearly free.** A `▎ ` prefix costs 2 and adds more scan-stopping contrast
than upgrading the alphabet does. When out of budget, add a marker, don't change the font.

## Traps

- **Bold breaks @-mentions.** LinkedIn's autocomplete matches plain text; a bolded name
  won't be found, and a mention that *is* set renders back to plain — leaving it visually
  out of line with bold neighbours. **Names stay plain. Always.**
- **Hashtags too.** `#𝗔𝗜` is not the tag `#AI`; it indexes as nothing.
- **Umlauts and accents have no styled codepoint.** Naive conversion leaves `ä` plain inside
  a bold run. Decompose (NFD), style the base letter, re-attach the mark. `ß` has no
  decomposition — it stays plain, and there is no fix. German headers: check them by eye.
- **Small caps have no X.** Unicode never assigned one, so `Ｘ` stays lowercase-plain in the
  middle of a small-caps run. Avoid small caps for words containing x.
- **Five alphabets have holes.** Script, fraktur, double-struck, serif-italic and their
  relatives have unassigned codepoints mid-range (Unicode scattered the missing letters into
  Letterlike Symbols). Base+offset arithmetic emits tofu for them. Map the holes explicitly
  or don't offer the alphabet.
- **Screen readers.** Bold math glyphs are read letter-by-letter or skipped entirely. Never
  style a whole sentence, never style the only copy of a fact.

## Style with intent

Styling is hierarchy, not decoration. More styles = less hierarchy.

- **Two levels, maximum:** section headers, plus one emphasis for the single number that
  carries the post. If everything is bold, nothing is.
- **The hook (line 1) is the scarcest real estate** — it's what shows before "see more".
  Bolding it costs double for the whole line; usually a stronger sentence beats a styled one.
- **Bullets:** `• ` (1 char) reads cleaner than emoji bullets and never renders as tofu.
- **Never style:** names, hashtags, links, or anything a reader may need to copy or search.

## Common mistakes

| Mistake | What happens |
|---|---|
| Glyphs pasted into the draft file | Grep/diff/spellcheck break; restyling means rewriting |
| Styling, then checking the count | Over the limit, and the cuts get made in panic |
| Bolding a name to make it stand out | The @-mention silently stops working |
| Script/fraktur "because it looks fancy" | Tofu boxes on some devices, unreadable aloud |
| A different style per section | Reads as noise; hierarchy disappears |
