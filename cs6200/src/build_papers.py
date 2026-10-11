"""Build the "beyond the notes" paper decks (21-31).

One deck per assigned paper, grouped under GIOS Papers::Midterm:: and
GIOS Papers::Final::. Cards come from cards/paper-cards-<tag>.jsonl, which are
authored by hand from the companion documents papers/papers-beyond-notes-<tag>.md
(not read by the build), and use the shared GIOS Basic / GIOS Cloze models.

Run from cs6200/src:
    uv run --no-project --with genanki==0.13.1 python build_papers.py [tag ...]

With no args builds every paper deck. Deck IDs are fixed so re-imports update
the existing deck and keep review history.
"""
import sys
from pathlib import Path

from cs6200deck import build_deck

HERE = Path(__file__).resolve().parent
CARDS = HERE / "cards"
DECKS = HERE.parent / "decks"

# tag -> (deck_id, deck_name, output stem). Midterm papers 21-24 (lecture order
# P2L2/P2L3, P2L4, P2L4, P2L5), final papers 25-31 (P3L1..P4L3).
PAPERS = {
    "birrell": (3912847581, "GIOS Papers::Midterm::21 Birrell (Programming with Threads)",
                "21-paper-birrell"),
    "eykholt": (3912847582, "GIOS Papers::Midterm::22 Eykholt (Multithreading the SunOS Kernel)",
                "22-paper-eykholt"),
    "stein-shah": (3912847583, "GIOS Papers::Midterm::23 Stein & Shah (Lightweight Threads)",
                   "23-paper-stein-shah"),
    "pai": (3912847584, "GIOS Papers::Midterm::24 Pai (Flash Web Server)",
            "24-paper-pai"),
    "fedorova": (3912847585, "GIOS Papers::Final::25 Fedorova (CMT Scheduler)",
                 "25-paper-fedorova"),
    "anderson": (3912847586, "GIOS Papers::Final::26 Anderson (Spin Lock Alternatives)",
                 "26-paper-anderson"),
    "popek-goldberg": (3912847587, "GIOS Papers::Final::27 Popek & Goldberg (Virtualizable Architectures)",
                       "27-paper-popek-goldberg"),
    "rosenblum-garfinkel": (3912847588, "GIOS Papers::Final::28 Rosenblum & Garfinkel (Virtual Machine Monitors)",
                            "28-paper-rosenblum-garfinkel"),
    "birrell-nelson": (3912847589, "GIOS Papers::Final::29 Birrell & Nelson (Implementing RPC)",
                       "29-paper-birrell-nelson"),
    "nelson": (3912847590, "GIOS Papers::Final::30 Nelson et al. (Caching in Sprite)",
               "30-paper-nelson"),
    "protic": (3912847591, "GIOS Papers::Final::31 Protic et al. (Distributed Shared Memory)",
               "31-paper-protic"),
}


def main():
    which = sys.argv[1:] or list(PAPERS)
    for tag in which:
        if tag not in PAPERS:
            sys.exit(f"unknown paper tag {tag!r}; known: {', '.join(PAPERS)}")
    for tag in which:
        deck_id, deck_name, stem = PAPERS[tag]
        build_deck(deck_id, deck_name, CARDS / f"paper-cards-{tag}.jsonl",
                   DECKS / f"{stem}.apkg")


if __name__ == "__main__":
    main()
