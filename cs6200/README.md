# CS 6200 (GIOS) Anki decks

Flashcards for Georgia Tech's CS 6200, Graduate Introduction to Operating
Systems. The decks follow the course's two halves: decks 01-08 cover the midterm
material (P1-P2), decks 09-20 cover the final material (P3-P4). In Anki they
appear under two top-level decks, `GIOS Midterm::` and `GIOS Final::`.

The card content is derived from the community lecture notes at
[omscs-notes.com](https://www.omscs-notes.com/operating-systems/welcome/), which
are maintained in the [omscs-notes-notes](https://github.com/m4ttsch/omscs-notes-notes)
repository (the `operating-systems/` directory), reworked into spaced-repetition
cards.

## Decks

| # | Deck | Cards | Covers |
|---|---|---:|---|
| 01 | P1L2 Introduction to Operating Systems | 88 | lecture |
| 02 | P2L1 Processes and Process Management | 90 | lecture |
| 03 | P2L2 Threads and Concurrency | 127 | lecture |
| 04 | P2L3 Threads Case Study: PThreads | 61 | lecture |
| 05 | P2L4 Thread Design Considerations | 132 | lecture |
| 06 | P2L5 Thread Performance Considerations | 107 | lecture |
| 07 | Midterm Questions and Answers | 128 | midterm review Q&A |
| 07a-c | Midterm Q&A, partitioned | 65 / 15 / 48 | same cards as 07, split by topic (Sample Midterm, OS Fundamentals, Threads and Flash) |
| 08 | Midterm Glossary | 246 | P1-P2 term glossary |
| 09 | P3L1 Scheduling | 132 | lecture |
| 10 | P3L2 Memory Management | 117 | lecture |
| 11 | P3L3 Inter-Process Communication | 70 | lecture |
| 12 | P3L4 Synchronization Constructs | 110 | lecture |
| 13 | P3L5 I/O Management | 81 | lecture |
| 14 | P3L6 Virtualization | 83 | lecture |
| 15 | P4L1 Remote Procedure Calls | 110 | lecture |
| 16 | P4L2 Distributed File Systems | 114 | lecture |
| 17 | P4L3 Distributed Shared Memory | 105 | lecture |
| 18 | P4L4 Datacenter Technologies | 117 | lecture |
| 19 | Final Questions and Answers | 245 | final review Q&A |
| 19a-j | Final Q&A, partitioned | 41 / 21 / 15 / 31 / 23 / 33 / 21 / 22 / 22 / 16 | same cards as 19, split by lecture (P3L1-P4L4) |
| 20 | Final Glossary | 368 | P3-P4 term glossary |
| 21 | Birrell, Programming with Threads | 175 | paper, beyond the notes |
| 22 | Eykholt, Multithreading the SunOS Kernel | 106 | paper, beyond the notes |
| 23 | Stein & Shah, Lightweight Threads | 110 | paper, beyond the notes |
| 24 | Pai, Flash Web Server | 99 | paper, beyond the notes |
| 25 | Fedorova, CMT Scheduler | 44 | paper, beyond the notes |
| 26 | Anderson, Spin Lock Alternatives | 65 | paper, beyond the notes |
| 27 | Popek & Goldberg, Virtualizable Architectures | 57 | paper, beyond the notes |
| 28 | Rosenblum & Garfinkel, Virtual Machine Monitors | 41 | paper, beyond the notes |
| 29 | Birrell & Nelson, Implementing RPC | 92 | paper, beyond the notes |
| 30 | Nelson et al., Caching in Sprite | 97 | paper, beyond the notes |
| 31 | Protic et al., Distributed Shared Memory | 102 | paper, beyond the notes |

The counts are notes, as reported by the build scripts; a cloze note with
several deletions shows as more than one card in Anki. The glossaries have one
note per defined term; "See ..." pointer entries produce none.

Decks 01-20 appear in Anki under `GIOS Midterm::` and `GIOS Final::`. The paper
decks (21-31) appear under `GIOS Papers::`, split into `Midterm` (21-24) and
`Final` (25-31) by which exam the paper belongs to.

**The lecture notes are sufficient for the course.** The lecture, Q&A, and
glossary decks (01-20) cover what you need for the exams. The paper decks
(21-31) are "beyond the notes": they capture what each assigned paper says that
the lecture does not, plus the places where a paper and the lecture diverge.
They are for your own background and interest, not required to do well on the
exams.

Deck 07 and decks 07a-c contain the **same cards** (07 is the whole set; 07a-c
re-partition it by topic: Sample Midterm, OS Fundamentals, Threads and Flash).
Decks 07a-c share note identities with 07, so import one or the other: if you
import both, each card stays in whichever deck you imported first and the other
decks are left empty. To switch, delete the first deck(s) before importing the
other. The same holds for the final: deck 19 is the whole final Q&A and decks
19a-j re-partition it by lecture (P3L1-P4L4). All other decks are disjoint.

The lecture decks and the glossary overlap in subject matter by design: the
glossary is a term-first ("Define: X") cut, the lecture decks are
mechanism/tradeoff cards. The Q&A decks (07, 19) likewise restate lecture
material as exam-style questions.

Each card shows a Source line, and carries tags, that depend on the deck type:

| Decks | Tags | Source line |
|---|---|---|
| Lecture (01-06, 09-18) | `pxly`, section slug, plus `paper` when drawn from a paper callout in the notes | the note's `##` section heading |
| Midterm Q&A (07, 07a-c) | `part-a`/`part-b`/`part-c`, question id (`a1`, `b3`, `c12`, ...), `midterm-review` | `Part A`, `Part B`, or `Part C` |
| Final Q&A (19, 19a-j) | `p3l1`..`p4l4`, `final-review` | the lecture code, `P3L1`..`P4L4` |
| Glossary (08, 20) | `pxly`, `glossary` | the lecture title, e.g. `P3L1 Scheduling` |
| Paper (21-31) | paper tag (e.g. `fedorova`), `paper-deck` | the companion document's section heading |

## Layout

```
cs6200/
  decks/                     # the 44 built .apkg (import these)
  src/
    cs6200deck.py            # shared genanki models (GIOS Basic / GIOS Cloze), validation, packaging
    build.py                 # builds the lecture decks (01-06, 09-18) and whole Q&A decks (07, 19)
    build_qa_split.py        # builds the Q&A sub-decks: midterm 07a-c and final 19a-j
    build_glossary.py        # builds the glossaries (08 midterm, 20 final) from glossary/*.md
    build_papers.py          # builds the paper decks (21-31) from cards/paper-cards-*.jsonl
    check_decks.py           # reports which built decks differ in content from the committed ones
    CARD_SPEC.md             # authoring rules for the lecture and Q&A card JSONL
    GLOSSARY_SPEC.md         # authoring rules for the glossary markdown
    PAPER_CARD_SPEC.md       # authoring rules for the paper-deck card JSONL
    cards/                   # per-deck card sources (JSONL): lecture, Q&A, and paper decks
    glossary/                # one glossary markdown per deck: midterm-glossary.md, final-glossary.md
    papers/                  # "beyond the notes" companion docs (hand-authoring source for the paper cards; not read by the build)
    media/                   # image cache, git-ignored, fetched on demand
```

## Building

Run from `src/` with [uv](https://docs.astral.sh/uv/). Each script writes its
`.apkg` into `../decks/`:

```
cd src

# Lecture decks (01-06, 09-18) and whole Q&A decks (07, 19)
uv run --no-project --with genanki==0.13.1 python build.py

# Q&A sub-decks: midterm 07a-c and final 19a-j
uv run --no-project --with genanki==0.13.1 python build_qa_split.py

# Glossaries: midterm (08) and final (20)
uv run --no-project --with genanki==0.13.1 python build_glossary.py

# Paper decks (21-31)
uv run --no-project --with genanki==0.13.1 python build_papers.py
```

A single script can also build a subset: `build.py`, `build_qa_split.py`,
`build_glossary.py`, and `build_papers.py` all take their deck keys as
arguments (deck stems, split keys `07`/`19`, glossary keys `08`/`20`, paper
tags).

Images are fetched from `assets.omscs.io` on first build into `src/media/`
(git-ignored) and embedded into the packages.

### Rebuilding and committing

genanki embeds timestamps, so every rebuild changes every `.apkg` file even
when no card changed. After rebuilding, run (from `src/`, standard library
only):

```
uv run --no-project python check_decks.py
```

It compares each deck with the committed version on what Anki imports (notes,
fields, tags, card count, deck names, media) and prints `SAME` or `DIFF` per
deck, then lists the `SAME` ones. Restore those with
`git checkout -- ../decks/<deck>.apkg`, so a commit contains only the decks
that really changed.

### How the sources relate to the decks

- **Decks 01-07 and 09-19** (lectures + whole Q&A): one card JSONL per deck in
  `cards/` (`cards-<stem>.jsonl`) is the source of truth; `build.py` maps each
  to its fixed deck ID and name.
- **Decks 07 and 19** are authored by hand from the exam review documents in
  the notes repository's `operating-systems/` directory. Deck 07:
  `midterm-sample-answers.md` (Part A, tags `a1`-`a6` = Questions 1-6) and
  `midterm-exam-review-questions.md` (Part B = its Part 1, `b1`-`b9` =
  Questions 1-9; Part C = its Part 2, `c1`-`c18` = Questions 10-27 in file
  order). Deck 19: `final-exam-review-questions.md`, with source and first tag
  = its `## P3L1`..`## P4L4` section. A fix to one of these documents must be
  carried into the matching cards by hand; the build reads only the JSONL.
- **Decks 07a-c and 19a-j** (Q&A sub-decks) are built by `build_qa_split.py`
  from the same `cards/` JSONL as decks 07 and 19, partitioned by tag (exam part
  for 07, lecture for 19), sharing the whole deck's note GUIDs.
- **Decks 08 and 20** (midterm and final glossaries) are built by
  `build_glossary.py` from `glossary/midterm-glossary.md` and
  `glossary/final-glossary.md` (one card per term).
- **Decks 21-31** (paper decks) are built from `cards/paper-cards-<tag>.jsonl`,
  authored by hand from the companion docs in `papers/`.

### Keeping review history

Re-importing a rebuilt deck updates existing notes in place, keyed by note
GUID. The GUID of a lecture, Q&A, or paper card is derived from its deck name,
`source`, and front (cloze: text); a glossary card's from its lecture and term
heading. Changing any of these makes the card arrive as a new card, without
its review history. Deck names and IDs never change. The per-type rules are in
`CARD_SPEC.md`, `GLOSSARY_SPEC.md`, and `PAPER_CARD_SPEC.md`.
