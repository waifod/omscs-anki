# Anki lecture-card generation spec

You generate flashcards for one OMSCS CS6200 lecture note. Output is one JSONL
file, one deck's worth of cards. This spec applies to every lecture deck in the
repo (midterm and final). The Q&A decks (07, 19) use the same format with the
conventions in "Q&A decks (07, 19)" below; paper decks follow PAPER_CARD_SPEC.md.

## Output format

One JSON object per line. Two card types:

Basic:
```
{"type":"basic","front":"<html>","back":"<html>","source":"<section heading>","tags":["<lecturetag>","<section-slug>"],"images":["UUID.png"]}
```
Cloze:
```
{"type":"cloze","text":"...{{c1::hidden}}...","extra":"<html or empty>","source":"<section heading>","tags":["<lecturetag>","<section-slug>"],"images":[]}
```

Rules for every field:
- `front`/`back`/`text`/`extra` are raw HTML. Allowed tags only: `<ul><li>`,
  `<ol><li>`, `<b>`, `<code>`, `<pre>`, `<br>`, `<img src="UUID.png">`, `<i>`.
  No markdown. No `<p>`.
- Escape literal ampersands as `&amp;` (e.g. "Stein &amp; Shah", "read &amp; write").
  Escape `<`/`>` that are not HTML tags as `&lt;`/`&gt;`.
- `source` is the lecture section heading the card is drawn from (the nearest
  `##` heading text, verbatim, no leading `#`). This is the only "source" value.
- `tags`: ALWAYS exactly `["<lecturetag>","<section-slug>"]` and, when the card
  is drawn from a `> **Paper (...)` callout, ALSO add `"paper"` as a third tag.
  - `<lecturetag>` is the deck's lecture tag (e.g. `p1l2`, `p3l1`).
  - `<section-slug>` = the section heading lowercased, non-alphanumerics to `-`,
    collapsed, trimmed (e.g. "Run To Completion Scheduling" -> `run-to-completion-scheduling`).
- `images`: list of local PNG basenames used on the card. EVERY basename listed
  here MUST also appear as `<img src="NAME">` in the HTML, and vice versa. Only
  reference an image that the note actually embeds in or near that section.
  Image URLs in the note look like `![](https://assets.omscs.io/notes/UUID.png)`;
  use only the `UUID.png` basename. Put the `<img>` on the `back` (basic) or
  `extra` (cloze), never on the front/question.

## Content rules

- Exam-focused, atomic cards. One fact or one tight cluster per card. Prefer
  many small Basic cards over few large ones. This is the dominant type.
- Use Cloze sparingly (a handful per deck), for crisp enumerations or
  definitional sentences where hiding one token tests recall. Number clozes
  `{{c1::}}`, `{{c2::}}`, etc.
- Cover the whole note section by section, in order. Include mechanisms,
  definitions, tradeoffs, numbers/formulas, worked reasoning, and diagrams.
- When a diagram carries the point (state machines, address layouts, protocol
  timelines), make a card whose answer embeds that image.
- Paper callouts (`> **Paper (<Author>):** ...` blocks) mark where the
  assigned paper corrects or adds to the lecture. Make a card for each such
  divergence, phrased so the answer states what the paper actually says, and
  tag it `paper`, e.g. front "lecture says X; what does <Author> say?", back
  states the paper's correction. (The exam review documents in the notes repo
  write the same divergences inline as `(Paper, <Author>: ...)` or
  `(Lecture framing: ...; Paper, <Author>: ...)`.)
- Do NOT invent facts. Everything must be grounded in the note text (including
  its callouts). Do not pull from outside the note.
- No em-dashes anywhere. Use commas, colons, or semicolons.

## Q&A decks (07, 19)

The Q&A decks restate lecture material as answers to the course's exam review
questions. Their authoring sources are documents in the notes repository
(`operating-systems/`); the build reads only the JSONL, so a fix to one of
these documents must be carried into the matching cards by hand.

- Deck 07 (midterm): `source` is `"Part A"`, `"Part B"`, or `"Part C"`; `tags`
  are `["part-x","<qid>","midterm-review"]`.
  - Part A: `midterm-sample-answers.md`, Questions 1-6, qid `a1`..`a6`.
  - Part B: `midterm-exam-review-questions.md` "Part 1: OS Fundamentals",
    Questions 1-9, qid `b1`..`b9`.
  - Part C: the same file's "Part 2", Questions 10-27, qid `c1`..`c18` in file
    order (`c1` = Question 10, `c18` = Question 27).
- Deck 19 (final): `final-exam-review-questions.md`. `source` is the question's
  section, `"P3L1"`..`"P4L4"` (the file's `## P3L1`..`## P4L4` headings);
  `tags` are `["p3lN"/"p4lN","final-review"]`, the lecture tag lowercased.
- The first tag that names a group (`part-a`/`part-b`/`part-c` for 07, `p3l1`..`p4l4`
  for 19) decides the sub-deck in `build_qa_split.py` (07a-c, 19a-j); a card
  without one fails the split build.
- Q&A cards overlap the lecture decks by design but must state each fact
  identically to the home lecture deck (same items, numbers, wording).
- No `paper` tag. A paper divergence the answer needs is written inline, e.g.
  `(Paper, Fedorova et al.: ...)`.

## Stability (review history)

Anki identifies a note by its GUID; a note with a new GUID arrives as a new card
and the old one, with its review history, is left orphaned.

- Lecture decks, whole Q&A decks (07, 19), and paper decks: GUID =
  `genanki.guid_for(deck name, source, front)` (`text` instead of `front` for
  cloze).
- Q&A sub-decks 07a-c and 19a-j: the same formula with the WHOLE deck's name
  (deck 07 or 19), so a card is the same note in the whole deck and in its
  sub-deck.
- Never rename a deck (its name is a GUID input; its ID is fixed in the build
  script).
- Editing a card's `front` (or cloze `text`) or `source` creates a new note.
  Avoid gratuitous rewording of fronts. When a note heading changes, either keep
  the card's old `source` or accept the reset knowingly.
- Backs, extras, tags, and images can change freely; re-importing updates the
  note in place.

## Style exemplars (from the real P2L4 deck)

- Q: `Signal handling: give an example of an OS-generated signal and its number.`
  A: `Accessing unallocated memory makes the OS generate <b>SIGSEGV</b>, signal 11.`
- Q: `Thread data structures at scale: what relationships must be maintained between ULTs, PCB, and KLTs?`
  A: `<ul><li>ULT library tracks all ULTs of a process...</li><li>Per process: the KLTs...</li><li>Per KLT: the process...</li></ul>`
- Paper card Q: `Death row: lecture says exiting threads go on death row. Which threads does Stein &amp; Shah say go there, and what happens to the others?`
  A: `Only <b>detached</b> threads go on death row. An undetached thread goes on a <b>zombie list</b>...`

Front strings often lead with a short topic prefix ("Signal handling:", a
lecture tag, or the concept) then the question. Keep answers tight.

## Volume

Roughly 70-150 cards for a substantial lecture, fewer for a short one. Let the
note's length and density decide; do not pad.
