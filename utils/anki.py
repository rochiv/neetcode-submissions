#!/usr/bin/env python3
"""Add or find Anki notes via AnkiConnect (localhost:8765). Anki must be open.

Basic card (fields are HTML; <code>…</code> etc. work):
  python3 utils/anki.py add "Front" "Back" --hook "vivid one-liner" \
      --source https://docs.python.org/3/... "Python docs, list.sort" --tags python blind75

Cloze card (each {{c1::…}} becomes its own card):
  python3 utils/anki.py add --cloze "x is {{c1::y}}" "back extra" --source URL "Label"

Diagram: --svg path/to/diagram.svg appends the file's SVG to the back
(draw with stroke/fill="currentColor" so it works in dark mode).
Footnote: --note "In Python: <code>Counter(s) == Counter(t)</code>".
Notes use the Tech:Basic / Tech:Cloze note types: explanation and Reference
(sources) are separate fields; all styling is in those note types' CSS.

Edit an existing note (only the parts you pass are replaced; --back is
rebuilt with --hook/--svg/--source just like add):
  python3 utils/anki.py update NOTE_ID --back "New back" --source URL "Label"
  python3 utils/anki.py update NOTE_ID --front "New front"
  python3 utils/anki.py update NOTE_ID --to-basic --front "Question?" --back "Answer" --source URL "Label"

Search (prints note id, deck, front):
  python3 utils/anki.py find '"deck:CS Pool" Counter'
"""
import argparse
import html
import json
import re
import sys
import urllib.request


def ac(action, **params):
    req = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        r = json.loads(urllib.request.urlopen("http://localhost:8765", req, timeout=10).read())
    except OSError:
        sys.exit("AnkiConnect not reachable: is Anki open?")
    if r["error"]:
        sys.exit(f"{action}: {r['error']}")
    return r["result"]


def compose_back(a):
    """-> (explanation HTML, reference HTML). Layout lives in the Tech:* note type CSS."""
    back = a.back
    if a.svg:
        back += f"<div class=fig>{open(a.svg).read()}</div>"
    if a.hook:
        back += f"<div class=hook>{a.hook}</div>"
    if a.note:
        back += f"<div class=note>{a.note}</div>"
    ref = " · ".join(f'<a href="{u}">{l}</a>' for u, l in zip(a.source[::2], a.source[1::2])) if a.source else None
    return back, ref


def fields_for(model, front, back, ref):
    names = ("Text", "Back Extra") if model == "Tech:Cloze" else ("Prompt", "Answer")
    vals = dict(zip(names, (front, back)), Reference=ref)
    return {k: v for k, v in vals.items() if v is not None}


def add(a):
    model = "Tech:Cloze" if a.cloze else "Tech:Basic"
    fields = fields_for(model, a.front, *compose_back(a))
    nid = ac("addNote", note={"deckName": a.deck, "modelName": model, "fields": fields, "tags": a.tags})
    print(f"added note {nid} to {a.deck}")


def update(a):
    info = ac("notesInfo", notes=[a.id])[0]
    back, ref = compose_back(a) if a.back is not None else (None, None)
    if a.to_basic:  # cloze -> Basic with an explicit question; needs --front and --back
        if a.front is None or a.back is None:
            sys.exit("--to-basic needs --front and --back")
        ac("updateNoteModel", note={"id": a.id, "modelName": "Tech:Basic", "tags": info["tags"],
                                    "fields": fields_for("Tech:Basic", a.front, back, ref)})
        ac("guiCheckDatabase")  # drops the extra {{c2::}} cards, which have no Basic template
    else:
        ac("updateNoteFields", note={"id": a.id, "fields": fields_for(info["modelName"], a.front, back, ref)})
    print(f"updated note {a.id}")


def find(a):
    ids = ac("findNotes", query=a.query)
    for n in ac("notesInfo", notes=ids[: a.limit]):
        front = next(iter(n["fields"].values()))["value"]
        text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", front))).strip()
        deck = ac("cardsInfo", cards=n["cards"][:1])[0]["deckName"]
        print(f"{n['noteId']}  [{deck}]  {text[:110]}")
    print(f"{len(ids)} match(es)" + (f", showing {a.limit}" if len(ids) > a.limit else ""))


p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
sub = p.add_subparsers(required=True)


def back_parts(sp):
    sp.add_argument("--hook", help="one vivid line, shown in italics")
    sp.add_argument("--note", help='footnote, e.g. "In Python: <code>Counter(s)</code>"')
    sp.add_argument("--svg", help="path to an .svg file to append to the back")
    sp.add_argument("--source", nargs="+", metavar="URL LABEL", help="URL/label pairs")


pa = sub.add_parser("add")
pa.add_argument("front")
pa.add_argument("back")
pa.add_argument("--cloze", action="store_true", help="front is cloze text")
back_parts(pa)
pa.add_argument("--tags", nargs="*", default=[])
pa.add_argument("--deck", default="CS")
pa.set_defaults(fn=add)
pu = sub.add_parser("update")
pu.add_argument("id", type=int)
pu.add_argument("--front")
pu.add_argument("--back")
pu.add_argument("--to-basic", action="store_true", help="convert a cloze note to Tech:Basic")
back_parts(pu)
pu.set_defaults(fn=update)
pf = sub.add_parser("find")
pf.add_argument("query", help="Anki search syntax")
pf.add_argument("--limit", type=int, default=15)
pf.set_defaults(fn=find)
args = p.parse_args()
if getattr(args, "source", None) and len(args.source) % 2:
    p.error("--source takes URL LABEL pairs")
args.fn(args)
