# Glossary authoring spec

Each half of the course has one glossary file: `glossary/midterm-glossary.md`
(deck 08, P1L2-P2L5) and `glossary/final-glossary.md` (deck 20, P3L1-P4L4).
Each file has one `## <LECTURE>` section per lecture containing `### Term`
entries. This spec covers writing a lecture's entries and maintaining the
merged file (cross-lecture links, stubs, paper corrections).

## Source of truth
Use ONLY the lecture notes, including their `> **Paper (<Author>):** ...`
callout blocks (where the assigned paper corrects or adds to the lecture). Do not pull
facts from outside the note. Standard, uncontroversial detail may be added only to
complete an obvious gap (e.g. a well-known field of a data structure the lecture
names but does not enumerate); when you do, keep it minimal and correct.

## Section heading
Start with exactly one line: `## <LECTURE LABEL> <Lecture Title>` where the label
is the lecture's `PxLy` code, e.g. `## P1L2 Introduction to Operating Systems` or
`## P3L1 Scheduling`. The label MUST match the regex `^## P\dL\d\b` (that is how
the packager finds the section).

## Entries
- One `### Term` per concept. Term headings are the glossary term, e.g.
  `### Timeslice`. A parenthetical alias is allowed: `### Runqueue (ready queue)`.
- Entries MUST be in ALPHABETICAL order within the section. Sort case-insensitively, ignoring leading punctuation (so `.x file` files under X).
- Define each term ONCE, in its home lecture (see "Maintaining the merged
  glossary"). A bare mention in a list does not merit a term; define things the
  lecture actually explains.
- After the heading, write the definition as one or more plain paragraph lines
  (no leading `-`). Paragraphs come BEFORE any list. Never put a paragraph after a
  list in the same entry (the packager rejects that).

## Allowed list structure (the packager is strict)
Only two indentation levels exist:
- top-level item:  `- text`
- sub-item:        `  - text` (exactly two spaces, under a top-level item)
No deeper nesting. No blank lines inside an entry are required, but blank lines
between entries are fine. Do not use tabs.

## Special item kinds (the packager parses these)
- Stores block: a top-level item whose text is `Stores:` (optionally
  `Stores (something):`), followed by sub-items listing what the structure holds.
  Use this ONLY for data structures / OS objects / tables that hold state.
    - Stores:
      - field one
      - field two
- Contrast: a top-level item `- Contrast: <text>` stating the opposing term.
- Lecture-vs-paper: when a `> **Paper (<Author>):**` callout corrects or clarifies the
  lecture, write the lecture's version in the definition (or in a
  `- Lecture version: ...` item), then a top-level item
  `- Paper correction (<Author>): <what the paper actually says>`. Pair any
  lecture-version statement with its paper correction so the entry is not left
  stating only the superseded version.
- Also-in item and "See ..." stubs: see "Maintaining the merged glossary".

## Maintaining the merged glossary
The header of `midterm-glossary.md` states the same conventions.
- Home entry: each concept has one canonical entry, normally in the first
  lecture that explains it. Material from later lectures is merged into it as
  top-level items prefixed with that lecture, e.g. `- (P2L4) ...`; where a later
  lecture says something different, keep both versions and state the
  difference. Implementation-specific structures (Solaris, Linux) keep their
  own entries and are linked from the canonical one.
- Also-in: the home entry ends with `- Also in: PxLy, PxLy.` listing the other
  lectures that discuss the concept, optionally with a short parenthetical
  saying how, e.g. `- Also in: P4L3 (as ...).` It is always the last item.
- Stub: when a later lecture has its own heading for a concept defined
  elsewhere, that entry is a single line `See <term> (PxLy).` (optionally
  followed by a short clause before the final period) pointing at the home
  entry. A stub produces no card.
- Fix facts in the home entry, not in a stub or Also-in line.
- Paper corrections use the label `Paper correction (<Author>):` with the
  author as the notes' callouts name it (`Birrell`, `Eykholt et al.`,
  `Stein & Shah`, `Pai et al.`, `Fedorova et al.`, `Anderson`,
  `Popek & Goldberg`, `Rosenblum & Garfinkel`, `Birrell & Nelson`,
  `Nelson et al.`, `Protic et al.`). Inside a merged `(PxLy)` item, write
  `Lecture version: ... Paper correction (<Author>): ...` inline.

## How an entry renders
One card per non-stub entry: front `Define: <Term> (PXLY)`, back = the entry's
paragraphs joined by `<br><br>`, followed directly by its items as one `<ul>`
(sub-items as a nested `<ul>`). A leading `Label:` on an item is bolded.
`` `code` `` becomes `<code>` and `**bold**` becomes `<b>`. No `<p>` tags are
emitted.

## Stability (review history)
A glossary note's GUID is `genanki.guid_for(<namespace>, "<pxly>-<slug of the
term heading>")` (namespaces `gios-midterm-glossary`, `gios-final-glossary`).
Renaming a `### Term` heading or moving the entry to another lecture section
creates a new note and orphans the old one with its review history. Definition
and item text can change freely. Never rename the decks.

## Style
- No em-dashes. No en-dashes. No exclamation points. No emoji. ASCII only.
- Plain prose, precise and dry. Define the term; do not address the reader.
- `code`/monospace for API names, flags, registers (e.g. `CR3`, `mmap`,
  `PTHREAD_PROCESS_SHARED`). `**bold**` is allowed sparingly inside definitions.

## Volume
Current lecture sections have 25-56 terms (about 40 is typical). Let the note's density
decide; cover the real vocabulary, do not pad with trivial or duplicate terms.

## Self-check before finishing
- Section heading matches `^## P\dL\d`.
- Every `###` term is unique within your section and the list is alphabetical.
- Only `- ` and `  - ` list markers; no paragraph follows a list in any entry.
- Any lecture-version statement is paired with its paper correction.
- No em-dashes or non-ASCII characters.
