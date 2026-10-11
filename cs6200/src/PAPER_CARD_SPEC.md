# Paper deck card generation spec ("beyond the notes")

You generate Anki cards for ONE "beyond the notes" companion document covering
one assigned CS6200 paper. Output is one JSONL file. Format matches the lecture
decks (same two models), with a few scope rules specific to paper decks.

## Source

Use ONLY the companion markdown you are given. It has these parts:
- Front matter / intro paragraph: paper title, authors, venue, PDF link.
- Per-section headings ("## Section N: ...", "## Abstract and front matter",
  etc.) with bullet points: the paper's own content that the lecture notes do
  NOT state. This is the primary card material.
- "## Covered in the notes": a recap of what the lecture already teaches. DO NOT
  make cards from this section; those facts live in the lecture decks already.
- "## Notes vs paper discrepancies": places where the lecture and paper differ,
  each with a verdict (LECTURE FRAMING / NOTES WRONG / NOT A REAL DISCREPANCY).
  Make cards from these: they are high-yield. Phrase so the answer states what
  the PAPER actually says, and (where relevant) how it differs from the lecture.
- "## Discrepancy sources" / reference lists: DO NOT make cards from these.

## Output format (one JSON object per line)

Basic: {"type":"basic","front":"<html>","back":"<html>","source":"<section>","tags":["<papertag>","paper-deck"],"images":[]}
Cloze: {"type":"cloze","text":"...{{c1::x}}...","extra":"<html>","source":"<section>","tags":["<papertag>","paper-deck"],"images":[]}

- `front`/`back`/`text`/`extra`: raw HTML. Allowed tags: `<ul><li>`, `<ol><li>`,
  `<b>`, `<code>`, `<pre>`, `<br>`, `<i>`. No markdown, no `<p>`.
- Escape literal `&` as `&amp;`, and stray `<`/`>` as `&lt;`/`&gt;`.
- `source`: the companion section heading the card is drawn from, verbatim
  without the leading `#` (e.g. "Section 4: Studying resource contention",
  "Notes vs paper discrepancies"). This mirrors how lecture-deck cards use the
  note's section heading.
- `tags`: ALWAYS exactly `["<papertag>", "paper-deck"]`. `<papertag>` is given to
  you (e.g. `fedorova`, `birrell-nelson`). Do not add other tags.
- `images`: always `[]` (companions embed no images).

## Content rules

- Exam-focused, atomic cards. One fact per card. The companions are dense with
  specific claims (numbers, named results, section-located facts); turn each
  distinct claim into its own card rather than bundling.
- Capture the paper's distinctive content: definitions the lecture omits, the
  paper's own experimental setup and quantified results, named systems/examples,
  authors' stated limitations and future work when substantive.
- For discrepancy cards, make the front pose the lecture's framing or the
  question, and the back state the paper's actual position; name the author
  (e.g. "what does Fedorova actually say?"). Do not reproduce the LECTURE
  FRAMING / NOTES WRONG verdict labels verbatim; convert them to plain Q&A.
- Do NOT invent facts. Everything must be grounded in the companion text.
- Do NOT make cards from the "Covered in the notes" or sources sections.
- No em-dashes. Use commas, colons, or semicolons.

## Volume

Let the companion's density decide: make as many cards as the companion needs
(the current decks range from 54 to 187 cards). Do not pad, but do not drop
substantive paper content either.

## Stability (review history)

A note's GUID is `genanki.guid_for(deck name, source, front)` (`text` for
cloze). Editing a card's `front` or `source`, or renaming the deck, creates a
new note and orphans the old one with its review history; backs can change
freely. When a companion heading changes, keep the card's old `source` or
accept the reset knowingly.

## Self-check before finishing

Re-read your file and confirm: every line is valid JSON; no blank lines; no raw
unescaped `&`; every `source` is a heading that appears in the companion; every
tag list is `["<papertag>","paper-deck"]`; `images` is `[]` everywhere.
