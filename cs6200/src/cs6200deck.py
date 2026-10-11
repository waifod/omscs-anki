"""Shared genanki models and packaging for the CS6200 (GIOS) Anki decks.

Two models with fixed IDs (GIOS Basic 1720154001, GIOS Cloze 1720154002) and a
shared CSS, used by every deck so re-imports update the existing models rather
than duplicating them.

Card JSONL schema (one object per line):
  basic: {"type":"basic","front":..,"back":..,"source":..,"tags":[..],"images":[..]}
  cloze: {"type":"cloze","text":..,"extra":..,"source":..,"tags":[..],"images":[..]}
front/back/text/extra are raw HTML. `images` lists local PNG basenames that MUST
also appear as <img src="name"> in the HTML; the packager verifies this and
attaches the files from MEDIA_DIR.

Images are not committed. They are fetched on demand from assets.omscs.io into
MEDIA_DIR (git-ignored) by ensure_image(); the .apkg embeds them, so using a
built deck needs no network, only rebuilding does.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

import genanki

HERE = Path(__file__).resolve().parent
MEDIA_DIR = HERE / "media"
ASSET_BASE = "https://assets.omscs.io/notes/"

MODEL_BASIC_ID = 1720154001
MODEL_CLOZE_ID = 1720154002

CSS = """
.card {font-family: -apple-system, Roboto, 'Segoe UI', sans-serif; font-size: 18px; line-height: 1.45;
  text-align: left; padding: 12px; color: #1d1d1f; background: #fff;}
img {max-width: 100%; height: auto; display: block; margin: 8px auto;}
pre, code {font-family: Menlo, Consolas, 'Roboto Mono', 'Courier New', monospace; font-size: 15px;}
pre {white-space: pre-wrap; word-wrap: break-word; overflow-x: auto; background: #f4f4f4; padding: 8px; border-radius: 6px;}
code {background: #f4f4f4; padding: 0 3px; border-radius: 3px;}
pre code {background: transparent; padding: 0;}
ul, ol {padding-left: 1.2em;}
.cloze {font-weight: bold; color: #0a58ca;}
.source {margin-top: 14px; font-size: 13px; color: #888;}
hr#answer {border: 0; border-top: 1px solid #ccc;}
.nightMode .card, .night_mode .card, .card.nightMode, .card.night_mode {color: #e6e6e6; background: #1e1e1e;}
.nightMode pre, .night_mode pre, .nightMode code, .night_mode code,
.card.nightMode pre, .card.night_mode pre, .card.nightMode code, .card.night_mode code {background: #2b2b2b;}
.nightMode pre code, .night_mode pre code, .card.nightMode pre code, .card.night_mode pre code {background: transparent;}
.nightMode .cloze, .night_mode .cloze, .card.nightMode .cloze, .card.night_mode .cloze {color: #6ea8fe;}
.nightMode .source, .night_mode .source, .card.nightMode .source, .card.night_mode .source {color: #999;}
.nightMode img, .night_mode img, .card.nightMode img, .card.night_mode img {background: #fff; padding: 4px; border-radius: 4px;}
"""

MODEL_BASIC = genanki.Model(
    MODEL_BASIC_ID,
    "GIOS Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
    templates=[{
        "name": "Card 1",
        "qfmt": "{{Front}}",
        "afmt": '{{FrontSide}}<hr id=answer>{{Back}}<div class=source>{{Source}}</div>',
    }],
    css=CSS,
)

MODEL_CLOZE = genanki.Model(
    MODEL_CLOZE_ID,
    "GIOS Cloze",
    fields=[{"name": "Text"}, {"name": "Extra"}, {"name": "Source"}],
    templates=[{
        "name": "Cloze",
        "qfmt": "{{cloze:Text}}",
        "afmt": '{{cloze:Text}}<br>{{Extra}}<div class=source>{{Source}}</div>',
    }],
    model_type=genanki.Model.CLOZE,
    css=CSS,
)

IMG_TAG_RE = re.compile(r'<img\s+src="([^"]+)"')
REQUIRED_BASIC = {"type", "front", "back", "source"}
REQUIRED_CLOZE = {"type", "text", "extra", "source"}

def ensure_image(name):
    """Return the local path for an image basename, fetching it if missing."""
    dst = MEDIA_DIR / name
    if dst.exists():
        return dst
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    url = ASSET_BASE + name
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            dst.write_bytes(resp.read())
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"failed to fetch image {name} from {url}: {exc}")
    return dst


def load_cards(path):
    """Parse and validate one JSONL file; return (cards, errors).

    Each returned card gets an `_images` list (declared plus referenced
    basenames); images are fetched later, by card_media().
    """
    cards, errors = [], []
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        where = f"{path.name}:{lineno}"
        if not line.strip():
            errors.append(f"{where}: blank line")
            continue
        try:
            card = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{where}: invalid JSON: {exc}")
            continue
        ctype = card.get("type")
        if ctype == "basic":
            missing = REQUIRED_BASIC - card.keys()
            html_fields = [card.get("front", ""), card.get("back", "")]
        elif ctype == "cloze":
            missing = REQUIRED_CLOZE - card.keys()
            html_fields = [card.get("text", ""), card.get("extra", "")]
        else:
            errors.append(f"{where}: bad type {ctype!r}")
            continue
        if missing:
            errors.append(f"{where}: missing keys {sorted(missing)}")
            continue
        joined = " ".join(html_fields)
        for m in re.finditer(r"&(?!(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)", joined):
            errors.append(f"{where}: raw '&' at col {m.start()}: "
                          f"...{joined[max(0, m.start()-15):m.start()+15]}...")
        declared = set(card.get("images", []))
        intag = set(IMG_TAG_RE.findall(joined))
        for img in declared - intag:
            errors.append(f"{where}: image {img!r} declared but no <img> tag")
        for img in intag - declared:
            errors.append(f"{where}: <img> {img!r} in HTML but not declared in images[]")
        card["_images"] = sorted(declared | intag)
        cards.append(card)
    return cards, errors


def load_or_exit(path):
    """load_cards(), printing the errors and exiting if there are any."""
    cards, errors = load_cards(Path(path))
    if errors:
        print(f"VALIDATION FAILED for {path}:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    return cards


def make_note(card, guid_name):
    """Build the genanki note for one card.

    The GUID is genanki.guid_for(guid_name, source, front) for basic cards and
    genanki.guid_for(guid_name, source, text) for cloze cards. guid_name is the
    deck name of the deck that owns the card (for the Q&A sub-decks, the whole
    deck's name), so changing it, the source, or the front creates a new note.
    """
    src = card["source"]
    tags = card.get("tags", [])
    if card["type"] == "basic":
        return genanki.Note(
            model=MODEL_BASIC, fields=[card["front"], card["back"], src],
            guid=genanki.guid_for(guid_name, src, card["front"]), tags=tags,
        )
    return genanki.Note(
        model=MODEL_CLOZE, fields=[card["text"], card["extra"], src],
        guid=genanki.guid_for(guid_name, src, card["text"]), tags=tags,
    )


def card_media(cards):
    """Return the sorted local paths of every image the cards use, fetching any missing."""
    return sorted({str(ensure_image(img)) for card in cards for img in card["_images"]})


def write_package(deck, media, output_path):
    """Write deck plus media file paths to output_path (an .apkg)."""
    pkg = genanki.Package(deck)
    pkg.media_files = list(media)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pkg.write_to_file(str(output_path))


def build_deck(deck_id, deck_name, jsonl_path, output_path):
    """Build a deck whose note GUIDs derive from (deck_name, source, front)."""
    cards = load_or_exit(jsonl_path)
    deck = genanki.Deck(deck_id, deck_name)
    for card in cards:
        deck.add_note(make_note(card, deck_name))
    media = card_media(cards)
    write_package(deck, media, output_path)
    n_basic = sum(1 for c in cards if c["type"] == "basic")
    n_cloze = len(cards) - n_basic
    print(f"{len(cards)} notes ({n_basic} basic, {n_cloze} cloze), "
          f"{len(media)} media -> {Path(output_path).name}")
