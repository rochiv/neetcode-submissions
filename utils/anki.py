#!/usr/bin/env python3
"""Add or find Anki notes via AnkiConnect (localhost:8765). Anki must be open.

Basic card (fields are HTML; <code>…</code> etc. work):
  python3 utils/anki.py add "Front" "Back" --hook "vivid one-liner" \
      --source https://docs.python.org/3/... "Python docs, list.sort" --tags python blind75

Cloze card (each {{c1::…}} becomes its own card):
  python3 utils/anki.py add --cloze "x is {{c1::y}}" "back extra" --source URL "Label"

Diagram: --svg path/to/diagram.svg appends the file's SVG to the back
(draw with stroke/fill="currentColor" so it works in dark mode).

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


def add(a):
    back = a.back
    if a.svg:
        back += "<br>" + open(a.svg).read()
    if a.hook:
        back += f"<br><i>{a.hook}</i>"
    if a.source:
        links = " · ".join(f'<a href="{u}">{l}</a>' for u, l in zip(a.source[::2], a.source[1::2]))
        back += f"<br><br><small>Source: {links}</small>"
    model, fields = (("Cloze", {"Text": a.front, "Back Extra": back}) if a.cloze
                     else ("Basic", {"Front": a.front, "Back": back}))
    nid = ac("addNote", note={"deckName": a.deck, "modelName": model, "fields": fields, "tags": a.tags})
    print(f"added note {nid} to {a.deck}")


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
pa = sub.add_parser("add")
pa.add_argument("front")
pa.add_argument("back")
pa.add_argument("--cloze", action="store_true", help="front is cloze text")
pa.add_argument("--hook")
pa.add_argument("--svg", help="path to an .svg file to append to the back")
pa.add_argument("--source", nargs="+", metavar="URL LABEL", help="URL/label pairs")
pa.add_argument("--tags", nargs="*", default=[])
pa.add_argument("--deck", default="CS")
pa.set_defaults(fn=add)
pf = sub.add_parser("find")
pf.add_argument("query", help="Anki search syntax")
pf.add_argument("--limit", type=int, default=15)
pf.set_defaults(fn=find)
args = p.parse_args()
if getattr(args, "source", None) and len(args.source) % 2:
    p.error("--source takes URL LABEL pairs")
args.fn(args)
