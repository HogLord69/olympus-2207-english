#!/usr/bin/env python3
"""Re-flow the Pip-Boy holodisks into English.

The holodisks are pre-wrapped: one screen line per string id, pane about 51
characters. The FE re-wrapped them for Russian, which runs longer, so the two
builds break lines in different places -- 1639 ids against 1627, drifting by
two or more inside a disk. Porting id-for-id therefore pastes English onto the
wrong lines, which is what scrambled every disk on the first attempt: FE id
3096 is "March 7, 2012" while old id 3096 is "the START-II agreement".

So this rebuilds the file instead of patching it.

PAIRING
  Disks are paired by thousand-block (FE 11000 <-> old 11000), which is
  reliable because both builds carry the same disks. Digit fingerprints --
  numbers survive translation, "3 марта 2151" and "March 3, 2151" share 3 and
  2151 -- are used only to CONFIRM. A disagreement is reported, never guessed
  past. Pairing by id, by position, and by digits alone were all tried first
  and all fail: ids drift, the FE has 52 contiguous runs against 31, and two
  disks carry too few numbers to fingerprint.

LAYOUT
  The FE's marker sequence (**END-DISK**, **END-PAR**, "...") is preserved in
  order. Between markers the old build's English is re-wrapped to the pane,
  with a leading date kept on its own line as the source does.

LENGTH
  A disk may need more lines than the FE reserved. Each disk owns its own
  thousand-block with 700-990 unused ids after it, so it simply gets more
  entries. Nothing is truncated.

    python pipboy_reflow.py --dry
    python pipboy_reflow.py
"""
import argparse
import difflib
import os
import re
import sys
import textwrap

sys.path.insert(0, r"C:\fallout-english-localization")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from falloutloc import dat_replace as dr
import oly_tool as T

MARKERS = {"...", "**END-DISK**", "**END-PAR**", ""}
WIDTHS = (49, 50, 51)
PANE = 51
TARGET = os.path.join(T.FE, "data", "text", "english", "game", "PIPBOY.MSG")

DATE = re.compile(r"^((?:January|February|March|April|May|June|July|August|"
                  r"September|October|November|December)\s+\d{1,2},?\s*\d{4}\.?"
                  r"|Date:[^.]{0,30}\d{4}\.?)\s+(?=[A-Z\[])")


def rows(data, enc):
    return [(int(sid), text.decode(enc, "replace"))
            for sid, _a, text, _s, _e in T.entries(data)]


def runs(rs):
    out, cur = [], []
    for r in rs:
        if cur and r[0] != cur[-1][0] + 1:
            out.append(cur); cur = []
        cur.append(r)
    if cur:
        out.append(cur)
    return out


def segments(rs):
    out, cur = [], []
    for sid, t in rs:
        if t.strip() in MARKERS:
            if cur:
                out.append(("text", cur)); cur = []
            out.append(("marker", [(sid, t)]))
        else:
            cur.append((sid, t))
    if cur:
        out.append(("text", cur))
    return out


def digits(rs):
    return re.findall(r"\d+", " ".join(t for _s, t in rs))


def wrap_para(en, width):
    """Wrap one paragraph, keeping a leading date on its own line."""
    en = " ".join(en.split())
    if not en:
        return []
    out = []
    m = DATE.match(en)
    if m:
        out.append(m.group(1).strip())
        en = en[m.end():]
    if en:
        out.extend(textwrap.wrap(en, width=width, break_long_words=False))
    return out


def build_disk(frun, orun):
    """Return (lines, note). Never truncates."""
    fsegs = segments(frun)
    osegs = [s for s in segments(orun) if s[0] == "text"]
    ftext = [s for s in fsegs if s[0] == "text"]

    if len(ftext) != len(osegs):
        # No safe paragraph mapping. Take the old build's own layout: it is
        # already wrapped to the pane and its markers already sit where the
        # English paragraphs break. Guessing a mapping is what scrambles disks.
        return [t for _s, t in orun], (f"old layout verbatim "
                                       f"(paragraphs {len(ftext)} vs {len(osegs)})")

    paras = [" ".join(t for _s, t in s[1]) for s in osegs]
    best = None
    for width in WIDTHS:
        seq, oi = [], 0
        for kind, items in fsegs:
            if kind == "marker":
                seq.append(items[0][1])
            else:
                seq.extend(wrap_para(paras[oi], width)); oi += 1
        if best is None or len(seq) < len(best[0]):
            best = (seq, width)
        if len(seq) <= len(frun):
            return seq, f"wrapped at {width}"
    return best[0], f"wrapped at {best[1]}, disk grew"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    fe_raw, fe, old_raw, old = T.load_sides()
    name = [k for k in fe if k.lower().endswith("game\\pipboy.msg")][0]
    fed = dr.content(fe_raw, fe[name])
    F = rows(fed, "cp1251")
    O = rows(dr.content(old_raw, old[name.lower()]), "cp1252")

    def block(sid):
        return sid // 1000 * 1000 if sid >= 1000 else sid

    # largest run per block on each side -- the disk itself, not the
    # one-line fragments that repeated ids create
    def by_block(all_runs):
        """-> {block: index into all_runs} for the largest run in each block."""
        out = {}
        for i, r in enumerate(all_runs):
            b = block(r[0][0])
            if b not in out or len(r) > len(all_runs[out[b]]):
                out[b] = i
        return out

    # Compute the runs ONCE and index into them. Calling runs() twice and
    # comparing by id() silently keeps every run, doubling the file.
    fruns, oruns = runs(F), runs(O)
    fidx, oidx = by_block(fruns), by_block(oruns)
    FB = {b: fruns[i] for b, i in fidx.items()}
    OB = {b: oruns[i] for b, i in oidx.items()}

    out_lines = []          # (id, text)
    disagree, grew, missing = [], [], []
    for b in sorted(FB):
        frun = FB[b]
        orun = OB.get(b)
        if orun is None:
            missing.append(b)
            out_lines.extend(frun)          # leave as-is
            continue
        seq, note = build_disk(frun, orun)

        fd, od = digits(frun), digits(orun)
        score = difflib.SequenceMatcher(None, fd, od).ratio() if fd and od else None
        if score is not None and score < 0.6:
            disagree.append((b, score))

        start = frun[0][0]
        if len(seq) > len(frun):
            nxt = min((x for x in FB if x > b), default=start + len(seq) + 1)
            if start + len(seq) >= nxt:
                print(f"  ! disk {b}: needs {len(seq)} lines, only "
                      f"{nxt - start} ids before the next disk -- skipped")
                out_lines.extend(frun)
                continue
            grew.append((b, len(frun), len(seq)))
        for i, line in enumerate(seq):
            out_lines.append((start + i, line))

    # anything not in a chosen run (the repeated-id fragments) is kept verbatim
    chosen = set(fidx.values())
    kept = [r for i, run in enumerate(fruns) if i not in chosen for r in run]
    # A repeated id can leave a one-line Russian fragment outside the disk we
    # rebuilt. Its English twin is already in the rebuild at the same id, so
    # take it from there rather than leaving Russian behind to shadow it.
    rebuilt = {}
    for sid, text in out_lines:
        rebuilt.setdefault(sid, text)
    fixed = []
    for sid, text in kept:
        if T.cyr(text.encode("cp1251", "replace")) and sid in rebuilt:
            text = rebuilt[sid]
        fixed.append((sid, text))
    out_lines.extend(fixed)
    out_lines.sort(key=lambda x: x[0])

    body = "".join(f"{{{sid}}}{{}}{{{text}}}\n" for sid, text in out_lines)
    data = body.encode("cp1251", "replace")

    over = [t for _s, t in out_lines if len(t) > PANE]
    print(f"disks rebuilt        : {len(FB) - len(missing)}/{len(FB)}")
    print(f"lines out            : {len(out_lines)} (was {len(F)})")
    print(f"disks that grew      : {len(grew)}  {[(b, a, c) for b, a, c in grew][:6]}")
    print(f"lines over {PANE} chars : {len(over)}")
    print(f"russian bytes left   : {T.cyr(data)}")
    if missing:
        print(f"  no donor block     : {missing}")
    if disagree:
        print(f"  DIGIT CHECK DISAGREES (block, score): {disagree}")

    if args.dry:
        print("\n[dry run] nothing written")
        return 0
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    with open(TARGET, "wb") as f:
        f.write(data)
    with open(TARGET, "rb") as f:
        back = f.read()
    print(f"\nwrote {TARGET}\nread-back matches: {back == data}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
