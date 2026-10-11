"""Build the partitioned Q&A sub-decks: midterm 07a-c and final 19a-j.

The whole Q&A decks (07, 19) are built by build.py. These sub-decks re-partition
the SAME cards into topic sub-decks: deck 07 by exam part (A/B/C) and deck 19 by
lecture group (P3L1..P4L4). Each card keeps the GUID it has in its whole deck
(derived from the whole deck's name, source, and front), so a card is the same
note in the whole deck and in its sub-deck. Import the whole deck OR its
sub-decks, not both. Cards are validated and their images attached exactly as
in build.py (cs6200deck.load_or_exit / card_media).

Run from cs6200/src:
    uv run --no-project --with genanki==0.13.1 python build_qa_split.py [07|19]

With no args, builds both splits.
"""
import sys
from pathlib import Path

import genanki

from cs6200deck import card_media, load_or_exit, make_note, write_package

HERE = Path(__file__).resolve().parent
CARDS = HERE / "cards"
DECKS = HERE.parent / "decks"

# Each split: the whole-deck JSONL stem, the whole-deck name (for GUIDs), the
# Anki sub-deck prefix, and the ordered partition key -> (letter, deck_id,
# title, output stem). A card goes to the group of its first tag that is a
# group key; a card with no such tag is an error.
SPLITS = {
    "07": {
        "jsonl": "07-midterm-questions-and-answers",
        "whole_name": "GIOS Midterm::07 Midterm Questions and Answers",
        "prefix": "GIOS Midterm::07 Q&A",
        "groups": {
            "part-a": ("a", 1205975849, "Sample Midterm", "07a-midterm-qa-part-a-sample-midterm"),
            "part-b": ("b", 1191435789, "OS Fundamentals", "07b-midterm-qa-part-b-os-fundamentals"),
            "part-c": ("c", 1545808825, "Threads and Flash", "07c-midterm-qa-part-c-threads-flash"),
        },
    },
    "19": {
        "jsonl": "19-final-questions-and-answers",
        "whole_name": "GIOS Final::19 Final Questions and Answers",
        "prefix": "GIOS Final::19 Q&A",
        "groups": {
            "p3l1": ("a", 3912847601, "P3L1 Scheduling", "19a-final-qa-p3l1-scheduling"),
            "p3l2": ("b", 3912847602, "P3L2 Memory Management", "19b-final-qa-p3l2-memory-management"),
            "p3l3": ("c", 3912847603, "P3L3 Inter-Process Communication", "19c-final-qa-p3l3-inter-process-communication"),
            "p3l4": ("d", 3912847604, "P3L4 Synchronization Constructs", "19d-final-qa-p3l4-synchronization-constructs"),
            "p3l5": ("e", 3912847605, "P3L5 I/O Management", "19e-final-qa-p3l5-io-management"),
            "p3l6": ("f", 3912847606, "P3L6 Virtualization", "19f-final-qa-p3l6-virtualization"),
            "p4l1": ("g", 3912847607, "P4L1 Remote Procedure Calls", "19g-final-qa-p4l1-remote-procedure-calls"),
            "p4l2": ("h", 3912847608, "P4L2 Distributed File Systems", "19h-final-qa-p4l2-distributed-file-systems"),
            "p4l3": ("i", 3912847609, "P4L3 Distributed Shared Memory", "19i-final-qa-p4l3-distributed-shared-memory"),
            "p4l4": ("j", 3912847610, "P4L4 Datacenter Technologies", "19j-final-qa-p4l4-datacenter-technologies"),
        },
    },
}


def build_split(spec):
    whole_name = spec["whole_name"]
    groups = spec["groups"]
    buckets = {g: [] for g in groups}
    path = CARDS / f"cards-{spec['jsonl']}.jsonl"
    for c in load_or_exit(path):
        key = next((t for t in c.get("tags", []) if t in groups), None)
        if key is None:
            raise SystemExit(f"{path.name}: card has no partition tag "
                             f"(tags={c.get('tags')}, source={c.get('source')})")
        buckets[key].append(c)

    total = 0
    for key, (letter, deck_id, title, stem) in groups.items():
        cards = buckets[key]
        sub_name = f"{spec['prefix']}::{letter.upper()} {title}"
        deck = genanki.Deck(deck_id, sub_name)
        for c in cards:
            deck.add_note(make_note(c, whole_name))
        media = card_media(cards)
        write_package(deck, media, DECKS / f"{stem}.apkg")
        print(f"{len(cards):4d} notes, {len(media)} media -> {stem}.apkg  [{sub_name}]")
        total += len(cards)
    print(f"  {spec['jsonl']} split total: {total}")


def main():
    which = sys.argv[1:] or list(SPLITS)
    for key in which:
        if key not in SPLITS:
            sys.exit(f"unknown split {key!r}; known: {', '.join(SPLITS)}")
    for key in which:
        build_split(SPLITS[key])


if __name__ == "__main__":
    main()
