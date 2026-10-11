"""Report which built decks differ in content from the committed (HEAD) version.

genanki embeds timestamps, so every rebuild changes every .apkg byte-for-byte
even when no card changed. This script compares each deck in ../decks/ with
`git show HEAD:cs6200/decks/<file>` on what Anki actually imports: notes
(GUID, fields, tags, model), card count, deck names, and media file names.

Run from cs6200/src (standard library only):
    uv run --no-project python check_decks.py

Prints one line per deck (SAME, DIFF with a short reason, or NEW when the deck
is not in HEAD), then the list of SAME decks. Restore those with
`git checkout -- <deck>` so a commit contains only decks that really changed.
"""
import io
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DECKS = HERE.parent / "decks"


def repo_root():
    out = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"not a git repository: {HERE}: {out.stderr.strip()}")
    return Path(out.stdout.strip())


def head_bytes(root, relpath):
    """Return the file's bytes at HEAD, or None if it is not in HEAD."""
    out = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{relpath}"],
                         capture_output=True)
    return out.stdout if out.returncode == 0 else None


def summary(data):
    """Return (notes, n_cards, deck_names, media_names) for .apkg bytes."""
    z = zipfile.ZipFile(io.BytesIO(data))
    fd, tmp = tempfile.mkstemp(suffix=".anki2")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(z.read("collection.anki2"))
        con = sqlite3.connect(tmp)
        try:
            notes = sorted(con.execute("select guid, flds, tags, mid from notes"))
            n_cards = con.execute("select count(*) from cards").fetchone()[0]
            decks = json.loads(con.execute("select decks from col").fetchone()[0])
        finally:
            con.close()
    finally:
        os.unlink(tmp)
    media = sorted(json.loads(z.read("media")).values())
    return notes, n_cards, sorted(d["name"] for d in decks.values()), media


def describe(old, new):
    o_notes, o_cards, o_decks, o_media = old
    n_notes, n_cards, n_decks, n_media = new
    reasons = []
    if o_notes != n_notes:
        og = {n[0]: n for n in o_notes}
        ng = {n[0]: n for n in n_notes}
        added = len(ng.keys() - og.keys())
        removed = len(og.keys() - ng.keys())
        changed = sum(1 for g in og.keys() & ng.keys() if og[g] != ng[g])
        reasons.append(f"notes {len(o_notes)}->{len(n_notes)} "
                       f"(+{added} -{removed} ~{changed})")
    if o_cards != n_cards:
        reasons.append(f"cards {o_cards}->{n_cards}")
    if o_decks != n_decks:
        reasons.append(f"deck names {o_decks}->{n_decks}")
    if o_media != n_media:
        reasons.append(f"media {len(o_media)}->{len(n_media)}")
    return reasons


def main():
    root = repo_root()
    same = []
    for path in sorted(DECKS.glob("*.apkg")):
        rel = path.resolve().relative_to(root.resolve()).as_posix()
        old_data = head_bytes(root, rel)
        if old_data is None:
            print(f"{path.name}: NEW (not in HEAD)")
            continue
        reasons = describe(summary(old_data), summary(path.read_bytes()))
        if reasons:
            print(f"{path.name}: DIFF " + "; ".join(reasons))
        else:
            print(f"{path.name}: SAME")
            same.append(path.name)
    print(f"\nSAME ({len(same)}):" + ("".join(f"\n  {n}" for n in same) or " none"))


if __name__ == "__main__":
    main()
