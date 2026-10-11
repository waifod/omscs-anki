"""Build the glossary decks (08 midterm, 20 final) from the glossary markdown.

Both glossaries use the same one-card-per-term form on the shared GIOS Basic
model, so they behave and look like every other deck. Each glossary is a single
markdown file with `## PxLy` sections and `### Term` entries; a term renders to
one card ("Define: Term") whose back is the entry body: the definition
paragraphs joined by <br><br>, followed directly by the entry's list (Stores,
Contrast, Paper correction, Also in, ...) as a <ul>. No <p> tags are emitted.
A stub entry ("See ...") produces no card.

Run from cs6200/src:
    uv run --no-project --with genanki==0.13.1 python build_glossary.py [08|20]

With no args, builds both.
"""
import html
import re
import sys
from pathlib import Path

import genanki

from cs6200deck import MODEL_BASIC

HERE = Path(__file__).resolve().parent
GLOSSARY_DIR = HERE / "glossary"
DECKS = HERE.parent / "decks"

# key -> (markdown file, deck_id, deck_name, guid namespace, allowed lecture tags)
GLOSSARIES = {
    "08": ("midterm-glossary.md", 2059384716, "GIOS Midterm::08 Glossary",
           "gios-midterm-glossary",
           ["p1l2", "p2l1", "p2l2", "p2l3", "p2l4", "p2l5"]),
    "20": ("final-glossary.md", 3912847572, "GIOS Final::20 Glossary",
           "gios-final-glossary",
           ["p3l1", "p3l2", "p3l3", "p3l4", "p3l5",
            "p3l6", "p4l1", "p4l2", "p4l3", "p4l4"]),
}

SECTION_RE = re.compile(r"^## (P\dL\d)\b(.*)$")
TERM_RE = re.compile(r"^### (.+?)\s*$")
TOP_ITEM_RE = re.compile(r"^- (.*)$")
SUB_ITEM_RE = re.compile(r"^  - (.*)$")
STUB_RE = re.compile(r"^See .+\.$")
LABEL_RE = re.compile(r"^([A-Z][A-Za-z ,/()-]{0,60}?(?: \([^)]*\))?):(\s|$)")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(text):
    out = []
    for i, part in enumerate(re.split(r"`([^`]*)`", text)):
        if i % 2:
            out.append(f"<code>{html.escape(part, quote=False)}</code>")
        else:
            esc = html.escape(part, quote=False)
            esc = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc)
            out.append(esc)
    return "".join(out)


def item_html(text):
    m = LABEL_RE.match(text)
    if m:
        rest = text[m.end(1) + 1:].lstrip()
        return f"<b>{inline(m.group(1))}:</b> {inline(rest)}".rstrip()
    return inline(text)


def parse(path):
    entries, lecture, title, cur = [], None, None, None
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        if line.startswith("## "):
            m = SECTION_RE.match(line)
            if not m:
                sys.exit(f"{path.name}:{lineno}: unrecognized section heading: {line}")
            lecture, title, cur = m.group(1).lower(), line[3:].strip(), None
            continue
        m = TERM_RE.match(line)
        if m:
            if lecture is None:
                sys.exit(f"{path.name}:{lineno}: term before any lecture section")
            cur = {"lecture": lecture, "title": title, "term": m.group(1),
                   "paragraphs": [], "items": [], "line": lineno}
            entries.append(cur)
            continue
        if cur is None or not line.strip():
            continue
        if (m := TOP_ITEM_RE.match(line)):
            cur["items"].append((m.group(1), []))
        elif (m := SUB_ITEM_RE.match(line)):
            if not cur["items"]:
                sys.exit(f"{path.name}:{lineno}: sub-item without parent")
            cur["items"][-1][1].append(m.group(1))
        elif line.startswith(" "):
            sys.exit(f"{path.name}:{lineno}: unsupported indentation: {line!r}")
        elif cur["items"]:
            sys.exit(f"{path.name}:{lineno}: paragraph after list in {cur['term']!r}")
        else:
            cur["paragraphs"].append(line)
    return entries


def is_stub(entry):
    return (not entry["items"] and len(entry["paragraphs"]) == 1
            and STUB_RE.match(entry["paragraphs"][0]) is not None)


def back_html(entry):
    """Paragraphs joined by <br><br>, then the item list (if any) as one <ul>."""
    parts = ["<br><br>".join(inline(p) for p in entry["paragraphs"])]
    if entry["items"]:
        lis = []
        for text, subs in entry["items"]:
            sub = ("<ul>" + "".join(f"<li>{item_html(s)}</li>" for s in subs) + "</ul>"
                   if subs else "")
            lis.append(f"<li>{item_html(text)}{sub}</li>")
        parts.append("<ul>" + "".join(lis) + "</ul>")
    return "".join(parts)


def build(key):
    fname, deck_id, deck_name, guid_ns, lectures = GLOSSARIES[key]
    path = GLOSSARY_DIR / fname
    entries = parse(path)
    seen = {}
    for e in entries:
        if e["term"] in seen:
            sys.exit(f"{fname}: duplicate term heading {e['term']!r} "
                     f"(lines {seen[e['term']]} and {e['line']})")
        seen[e["term"]] = e["line"]

    deck = genanki.Deck(deck_id, deck_name)
    n = stubs = 0
    for e in entries:
        if e["lecture"] not in lectures:
            sys.exit(f"{fname}: unexpected lecture {e['lecture']!r} at line {e['line']}")
        if is_stub(e):
            stubs += 1
            continue
        back = back_html(e)
        if not back:
            sys.exit(f"{fname}: empty back for {e['term']!r} (line {e['line']})")
        lec = e["lecture"]
        deck.add_note(genanki.Note(
            model=MODEL_BASIC,
            fields=[f"Define: {inline(e['term'])} ({lec.upper()})", back, e["title"]],
            guid=genanki.guid_for(guid_ns, f"{lec}-{slugify(e['term'])}"),
            tags=[lec, "glossary"],
        ))
        n += 1

    out = DECKS / ("08-midterm-glossary.apkg" if key == "08"
                   else "20-final-glossary.apkg")
    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(deck).write_to_file(str(out))
    print(f"{len(entries)} terms, {stubs} stubs, {n} cards -> {out.name}")


def main():
    which = sys.argv[1:] or list(GLOSSARIES)
    for key in which:
        if key not in GLOSSARIES:
            sys.exit(f"unknown glossary {key!r}; known: {', '.join(GLOSSARIES)}")
    for key in which:
        build(key)


if __name__ == "__main__":
    main()
