#!/usr/bin/env python3
"""Port ScrnSet.msg -- the screen-settings UI, which lives outside master.dat.

The FE carries this file in both f2_res.dat and sfall.dat; the sfall copy is
the superset (100 ids vs 94), so that is the base. The English donor is the old
build's f2_res.dat copy. Output is a loose override at
data/text/english/game/ScrnSet.msg, which the engine reads ahead of both
archives because olympus.cfg sets master_patches=data.
"""
import os, sys
sys.path.insert(0, r"C:\fallout-english-localization")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from falloutloc import dat_replace as dr
import oly_tool as T

WANT = r"text\english\game\scrnset.msg"
TARGET = os.path.join(T.FE, "data", "text", "english", "game", "ScrnSet.msg")

def get(path):
    raw, ents = dr.read_entries(path)
    for e in ents:
        if e["name"].replace("/", "\\").lower() == WANT:
            return dr.content(raw, e)

base = get(os.path.join(T.FE, "sfall.dat"))
donor = get(os.path.join(T.OLD, "f2_res.dat"))
if base is None or donor is None:
    sys.exit("missing ScrnSet source")

new, ported, left = T.port_file(base, donor)
os.makedirs(os.path.dirname(TARGET), exist_ok=True)
with open(TARGET, "wb") as f:
    f.write(new)
with open(TARGET, "rb") as f:
    back = f.read()
print(f"ported {ported} strings, {left} still russian")
print(f"wrote {TARGET}")
print(f"read-back matches: {back == new}")
