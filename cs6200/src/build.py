"""Build the lecture decks and the whole Q&A decks (01-07, 09-19).

Covers every deck whose cards live as one JSONL per deck in cards/: the midterm
lecture decks (01-06) and midterm Q&A (07), and the final lecture decks (09-18)
and final Q&A (19). The glossaries (08, 20), the Q&A sub-decks (07a-c, 19a-j),
and the paper decks (21-31) have their own build scripts.

Run from cs6200/src:
    uv run --no-project --with genanki==0.13.1 python build.py [stem ...]

With no args builds every deck below. Images are fetched on demand (see
cs6200deck). Deck IDs are fixed so re-imports update the existing deck and keep
review history.
"""
import sys
from pathlib import Path

from cs6200deck import build_deck

HERE = Path(__file__).resolve().parent
CARDS = HERE / "cards"
DECKS = HERE.parent / "decks"

# jsonl stem (cards-<stem>.jsonl) -> (deck_id, deck_name). Output .apkg is <stem>.apkg.
DECKS_SPEC = {
    # Midterm lectures (01-06) and midterm Q&A (07). IDs/names preserved from
    # the original decks so re-imports update in place.
    "01-p1l2-introduction-to-operating-systems":
        (4230638133, "GIOS Midterm::01 P1L2 Introduction to Operating Systems"),
    "02-p2l1-processes-and-process-management":
        (1657913933, "GIOS Midterm::02 P2L1 Processes and Process Management"),
    "03-p2l2-threads-and-concurrency":
        (2098297203, "GIOS Midterm::03 P2L2 Threads and Concurrency"),
    "04-p2l3-threads-case-study-pthreads":
        (1758609766, "GIOS Midterm::04 P2L3 Threads Case Study PThreads"),
    "05-p2l4-thread-design-considerations":
        (1706024952, "GIOS Midterm::05 P2L4 Thread Design Considerations"),
    "06-p2l5-thread-performance-considerations":
        (3262242307, "GIOS Midterm::06 P2L5 Thread Performance Considerations"),
    "07-midterm-questions-and-answers":
        (1199631218, "GIOS Midterm::07 Midterm Questions and Answers"),
    # Final lectures (09-18) and final Q&A (19).
    "09-p3l1-scheduling":
        (3912847561, "GIOS Final::09 P3L1 Scheduling"),
    "10-p3l2-memory-management":
        (3912847562, "GIOS Final::10 P3L2 Memory Management"),
    "11-p3l3-inter-process-communication":
        (3912847563, "GIOS Final::11 P3L3 Inter-Process Communication"),
    "12-p3l4-synchronization-constructs":
        (3912847564, "GIOS Final::12 P3L4 Synchronization Constructs"),
    "13-p3l5-io-management":
        (3912847565, "GIOS Final::13 P3L5 I/O Management"),
    "14-p3l6-virtualization":
        (3912847566, "GIOS Final::14 P3L6 Virtualization"),
    "15-p4l1-remote-procedure-calls":
        (3912847567, "GIOS Final::15 P4L1 Remote Procedure Calls"),
    "16-p4l2-distributed-file-systems":
        (3912847568, "GIOS Final::16 P4L2 Distributed File Systems"),
    "17-p4l3-distributed-shared-memory":
        (3912847569, "GIOS Final::17 P4L3 Distributed Shared Memory"),
    "18-p4l4-datacenter-technologies":
        (3912847570, "GIOS Final::18 P4L4 Datacenter Technologies"),
    "19-final-questions-and-answers":
        (3912847571, "GIOS Final::19 Final Questions and Answers"),
}


def main():
    which = sys.argv[1:] or list(DECKS_SPEC)
    for stem in which:
        if stem not in DECKS_SPEC:
            sys.exit(f"unknown deck {stem!r}; known: {', '.join(DECKS_SPEC)}")
    for stem in which:
        deck_id, deck_name = DECKS_SPEC[stem]
        build_deck(deck_id, deck_name, CARDS / f"cards-{stem}.jsonl",
                   DECKS / f"{stem}.apkg")


if __name__ == "__main__":
    main()
