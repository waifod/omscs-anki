# omscs-anki

Anki flashcard decks for [OMSCS](https://omscs.gatech.edu/) courses, with the
sources and build scripts that generate them.

Each course lives in its own folder, keyed by its course identifier:

| Folder | Course |
|---|---|
| [`cs6200/`](cs6200/) | CS 6200 Graduate Introduction to Operating Systems (GIOS) |

Within a course folder, `decks/` holds the built `.apkg` files you import into
Anki, and `src/` holds the card sources and the scripts that build them. See the
per-course README for the deck list and build instructions.

## Using the decks

Download a `.apkg` from the course's `decks/` folder and import it into Anki
(File > Import, or open the file). Images are embedded in the package, so no
network access is needed to study.

Deck and note identities (deck IDs, model IDs, note GUIDs) are fixed, so
re-importing an updated deck updates the existing cards in place rather than
creating duplicates. This preserves your review history for cards whose front
(and source) did not change; a reworded card arrives as a new card.

## Rebuilding

The decks are reproducible from the sources in each `src/`. The scripts use
[genanki](https://github.com/kerrickstaley/genanki) and are run with
[uv](https://docs.astral.sh/uv/):

```
cd cs6200/src
uv run --no-project --with genanki==0.13.1 python build.py
```

Lecture diagrams are fetched on demand from `assets.omscs.io` into a
git-ignored local cache on first build; they are then embedded in the `.apkg`.

## Provenance

The card content is derived from the public community lecture notes at
[omscs-notes.com](https://www.omscs-notes.com/) (the
[omscs-notes-notes](https://github.com/m4ttsch/omscs-notes-notes) repository),
reorganized into spaced-repetition cards.
