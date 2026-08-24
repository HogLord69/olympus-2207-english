#!/usr/bin/env python3
"""Olympus 2207 English localization -- port and verify.

The newest Russian Fixed Edition and an older English build are the same game.
Roughly four fifths of the Russian text already exists in English in the older
build, so the bulk of this job is a port, not a translation.

    python oly_tool.py survey     what is where, and how much each side covers
    python oly_tool.py port       write the English strings into the FE
    python oly_tool.py verify     read the game back off disk, report Russian
    python oly_tool.py remaining  what still needs translating, most-repeated first

Output is loose files under
    C:\\Olympus 2207 (FE)\\data\\text\\english\\...
which the engine loads ahead of master.dat because olympus.cfg sets
master_patches=data. No archive is ever rewritten.

HOW THE PORT DECIDES
--------------------
Per string, never per file. The FE's own structure is kept and only the text
field is replaced, so anything the FE added that the old build never had is
preserved as Russian for translation rather than silently dropped.

A string is ported when all of these hold:
  * the FE string is Russian
  * the old build has the same id at the same occurrence index
  * that string is non-empty and contains no Cyrillic

OCCURRENCE INDEX, NOT JUST ID
-----------------------------
22 of these files repeat a string id, carrying different lines under the same
number. Reading a .msg into a dict keyed by id silently drops all but the last,
which is how ten Russian barks survived a "100% complete" build on a sibling
project. Everything here works on occurrence lists.

WHY ID MATCHING IS SAFE HERE
----------------------------
Across *different* games it would not be -- every total conversion renumbers.
These are two builds of one game, and it was checked before relying on it: the
audio field (language-independent, usually a sound filename) agrees on
6463/6465 shared ids, 99.97%, with no file below 95%. Nothing was renumbered.
`survey` re-runs that check.
"""
import os
import re
import sys

sys.path.insert(0, r"C:\fallout-english-localization")
from falloutloc import dat_replace as dr

FE = r"C:\Olympus 2207 (FE)"
OLD = r"F:\GOG Games\Fallout 2 - Copy"

ENTRY = re.compile(rb"\{(\d+)\}\{([^}]*)\}\{([^}]*)\}", re.S)


def cyr(bs):
    """Count cp1251 Cyrillic bytes. 0xC0-0xFF, plus 0xA8/0xB8 for Yo."""
    return sum(1 for b in bs if b >= 0xC0 or b in (0xA8, 0xB8))


def entries(data):
    """Every occurrence in file order: (id, audio, text, text_start, text_end)."""
    return [(m.group(1).decode(), m.group(2), m.group(3), m.start(3), m.end(3))
            for m in ENTRY.finditer(data)]


def by_occurrence(data):
    """{(id, nth): (audio, text)} -- survives repeated ids."""
    out, seen = {}, {}
    for sid, audio, text, _, _ in entries(data):
        n = seen.get(sid, 0)
        out[(sid, n)] = (audio, text)
        seen[sid] = n + 1
    return out


def index(path):
    raw, ents = dr.read_entries(path)
    return raw, {e["name"].replace("/", "\\"): e
                 for e in ents if e["name"].lower().endswith(".msg")}


def load_sides():
    fe_raw, fe = index(os.path.join(FE, "master.dat"))
    old_raw, old = index(os.path.join(OLD, "master.dat"))
    old_lower = {k.lower(): v for k, v in old.items()}
    return fe_raw, fe, old_raw, old_lower


def port_file(fe_data, old_data):
    """Return (new_bytes, ported, still_russian)."""
    donor = by_occurrence(old_data) if old_data is not None else {}
    out, prev = bytearray(), 0
    ported = left = 0
    seen = {}
    for sid, _audio, text, a, b in entries(fe_data):
        n = seen.get(sid, 0)
        seen[sid] = n + 1
        if not cyr(text):
            continue
        give = donor.get((sid, n))
        if give and give[1].strip() and not cyr(give[1]):
            out += fe_data[prev:a] + give[1]
            prev = b
            ported += 1
        else:
            left += 1
    out += fe_data[prev:]
    return bytes(out), ported, left


# ---------------------------------------------------------------- survey
def cmd_survey():
    fe_raw, fe, old_raw, old = load_sides()
    print(f"FE  master.dat : {len(fe)} .msg")
    print(f"old master.dat : {len(old)} .msg")

    tot = rus = portable = 0
    audio_ok = audio_tot = 0
    dupes = []
    buckets = {"full": 0, "partial": 0, "none": 0, "missing": 0}
    for name, e in sorted(fe.items()):
        fd = dr.content(fe_raw, e)
        fents = entries(fd)
        tot += len(fents)
        r = sum(1 for x in fents if cyr(x[2]))
        rus += r
        if len(set(x[0] for x in fents)) != len(fents):
            dupes.append(name)
        oe = old.get(name.lower())
        if oe is None:
            buckets["missing"] += 1
            continue
        od = dr.content(old_raw, oe)
        _, p, _ = port_file(fd, od)
        portable += p
        buckets["full" if p >= r else ("partial" if p else "none")] += 1
        donor = by_occurrence(od)
        seen = {}
        for sid, audio, _t, _a, _b in fents:
            n = seen.get(sid, 0); seen[sid] = n + 1
            g = donor.get((sid, n))
            if g and (audio.strip() or g[0].strip()):
                audio_tot += 1
                audio_ok += audio.strip().lower() == g[0].strip().lower()

    print(f"\nFE strings        : {tot}")
    print(f"  Russian         : {rus}")
    print(f"  portable as-is  : {portable}  ({100*portable/max(rus,1):.1f}% of Russian)")
    print(f"  needs translating: {rus - portable}")
    print(f"\nfiles: {buckets['full']} fully covered, {buckets['partial']} partly, "
          f"{buckets['none']} no help, {buckets['missing']} absent from old build")
    print(f"\nid alignment check (audio field): {audio_ok}/{audio_tot} "
          f"({100*audio_ok/max(audio_tot,1):.2f}%)")
    print(f"files with repeated ids: {len(dupes)}")


# ---------------------------------------------------------------- port
def cmd_port(dry=False):
    fe_raw, fe, old_raw, old = load_sides()
    out_root = os.path.join(FE, "data")
    files = ported = left = written = 0
    for name, e in sorted(fe.items()):
        fd = dr.content(fe_raw, e)
        oe = old.get(name.lower())
        od = dr.content(old_raw, oe) if oe is not None else None
        new, p, l = port_file(fd, od)
        ported += p
        left += l
        files += 1
        if dry or p == 0:
            continue
        dest = os.path.join(out_root, name.replace("\\", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if os.path.exists(dest) and not os.path.exists(dest + ".orig"):
            with open(dest, "rb") as f:
                orig = f.read()
            with open(dest + ".orig", "wb") as f:
                f.write(orig)
        with open(dest, "wb") as f:
            f.write(new)
        # verify by reading back off disk, not by trusting the transform
        with open(dest, "rb") as f:
            disk = f.read()
        if disk != new:
            print(f"  ! {name}: write-back mismatch")
            continue
        written += 1
    tag = "[dry run] " if dry else ""
    print(f"{tag}{files} files scanned, {written} written")
    print(f"{tag}ported {ported} strings, {left} still Russian")


# ---------------------------------------------------------------- verify
def cmd_verify():
    """Read the game the way the engine will: loose file wins over the archive."""
    fe_raw, fe, _, _ = load_sides()
    tot = rus = 0
    worst = []
    for name, e in sorted(fe.items()):
        loose = os.path.join(FE, "data", name.replace("\\", os.sep))
        if os.path.isfile(loose):
            with open(loose, "rb") as f:
                data = f.read()
        else:
            data = dr.content(fe_raw, e)
        ents = entries(data)
        tot += len(ents)
        r = sum(1 for x in ents if cyr(x[2]))
        rus += r
        if r:
            worst.append((r, len(ents), name))
    print(f"\n  scanned {tot} strings across {len(fe)} .msg files")
    if not rus:
        print("  no russian left on disk - the english build is complete")
        return
    print(f"  RUSSIAN STILL ON DISK: {rus} strings in {len(worst)} files\n")
    for r, t, name in sorted(worst, reverse=True)[:25]:
        print(f"    {r:6}/{t:<6} {name}")


# ---------------------------------------------------------------- remaining
def cmd_remaining(limit=40):
    fe_raw, fe, _, _ = load_sides()
    uniq = {}
    for name, e in sorted(fe.items()):
        loose = os.path.join(FE, "data", name.replace("\\", os.sep))
        if os.path.isfile(loose):
            with open(loose, "rb") as f:
                data = f.read()
        else:
            data = dr.content(fe_raw, e)
        for sid, _a, text, _s, _t in entries(data):
            if cyr(text):
                k = re.sub(rb"\s+", b" ", text).strip()
                uniq.setdefault(k, []).append(name)
    print(f"{sum(len(v) for v in uniq.values())} russian strings, "
          f"{len(uniq)} unique\n")
    for k, where in sorted(uniq.items(), key=lambda x: -len(x[1]))[:limit]:
        print(f"  [{len(where):4}x] {k.decode('cp1251','replace')[:88]}")


# ---------------------------------------------------------------- translate
def load_glossary():
    """{normalised russian: english} from every tr/t*.py.

    Keyed by text rather than by (file, id) so one entry resolves every
    occurrence everywhere -- the three identical death cries in COMBATAI share
    a single key. Keys are normalised on load, so a batch can be written with
    the russian copied verbatim, trailing spaces and all.
    """
    import glob as _glob
    T = {}
    for path in sorted(_glob.glob(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "tr", "t*.py"))):
        ns = {}
        exec(open(path, encoding="utf-8").read(), ns)
        for k, v in ns.get("T", {}).items():
            T[re.sub(r"\s+", " ", k).strip()] = v
    return T


def cmd_translate(dry=False):
    """Apply the glossary to whatever russian is left, occurrence-aware."""
    gloss = load_glossary()
    fe_raw, fe, _, _ = load_sides()
    files = applied = missing = 0
    unresolved = {}
    for name, e in sorted(fe.items()):
        dest = os.path.join(FE, "data", name.replace("\\", os.sep))
        data = open(dest, "rb").read() if os.path.isfile(dest) else dr.content(fe_raw, e)
        hits = []
        for sid, _audio, text, a, b in entries(data):
            if not cyr(text):
                continue
            key = re.sub(r"\s+", " ", text.decode("cp1251", "replace")).strip()
            en = gloss.get(key)
            if en is None:
                unresolved[key] = unresolved.get(key, 0) + 1
                missing += 1
                continue
            hits.append((a, b, en))
        if not hits:
            continue
        out, prev = bytearray(), 0
        for a, b, en in hits:
            out += data[prev:a] + en.encode("cp1251", "replace")
            prev = b
        out += data[prev:]
        applied += len(hits)
        files += 1
        if dry:
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(bytes(out))
        with open(dest, "rb") as f:
            if f.read() != bytes(out):
                log = print
                log(f"  ! {name}: write-back mismatch")
    tag = "[dry run] " if dry else ""
    print(f"{tag}glossary entries: {len(gloss)}")
    print(f"{tag}applied {applied} strings across {files} files")
    print(f"{tag}unmatched russian: {missing} ({len(unresolved)} unique)")
    for k, n in sorted(unresolved.items(), key=lambda x: -x[1])[:12]:
        print(f"    [{n}x] {k[:80]}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "survey"
    if   cmd == "survey":    cmd_survey()
    elif cmd == "port":      cmd_port()
    elif cmd == "dry":       cmd_port(dry=True)
    elif cmd == "verify":    cmd_verify()
    elif cmd == "remaining": cmd_remaining()
    elif cmd == "translate": cmd_translate()
    elif cmd == "trydry":    cmd_translate(dry=True)
    else: sys.exit(f"unknown command: {cmd}")
