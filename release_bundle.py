#!/usr/bin/env python3
"""Build the distributable archive: a single self-contained, ready-to-play folder.

    python release.py --out "C:\\sotj-release"

Produces Fallout-Story-of-the-Jackal-English.zip, which extracts to one folder
you launch from directly. The English text is already applied -- this packages
the installed state, it does not translate anything. Run
`python oly_tool.py verify` first; this script refuses to build if any Russian
is left on disk.

The game is ~640 MB, so it fits GitHub's 2 GB per-asset limit in one piece.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

GAME = r"C:\Olympus 2207 (FE)"
NAME = "Olympus-2207-English"
EXE = "OLYMPUS.EXE"

SEVENZIP = [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]
ASSET_LIMIT = 2 * 1000 ** 3

# Backups and working files a player has no use for.
SKIP_FILES = ["*.orig", "*.dmp", "sfall-log*.txt", "*.log"]
SKIP_DIRS = ["uninstall"]

LAUNCHER = """@echo off
rem Olympus 2207 -- English. Must run from its own folder.
cd /d "%~dp0"
start "" "{exe}"
"""

READ_ME = """FALLOUT: STORY OF THE JACKAL -- ENGLISH
=======================================

Fixed Edition, build 03.08.26 - a rebuild by Foxx


TO PLAY
-------

  Double-click:  Play Olympus 2207.bat

Nothing to install, nothing to configure. Saves stay in this folder.


THE GAME
--------

A total conversion for Fallout 2 by NEBESA GAMES, built between 2010 and
2015, and rebuilt by Foxx as this Fixed Edition.


THIS TRANSLATION
----------------

42,296 strings across 270 files. No Russian left.

Most of this is a port: an older English build of Olympus already existed,
and the Fixed Edition is the same game, newer. 35,603 strings were carried
across per string, the Pip-Boy holodisks were re-flowed to the new line
layout, and 98 strings the Fixed Edition added were translated.

Verified by reading every file back off disk through the engine's own load
order: no Russian remains.


NOTE
----

Turn OFF vertical sync in your graphics driver settings, or the game shows
graphical glitches. That is the Fixed Edition's own advice.

Bugs and rough edges are the game's own. Anything that reads wrong in
English is ours - please report it.


If the game opens to a black screen, right-click {exe}, choose
Properties -> Compatibility, and tick "Disable fullscreen optimizations".

See CREDITS.txt.
"""

CREDITS = """CREDITS
=======

OLYMPUS 2207
    NEBESA GAMES, 2010-2015.
      Artem "RAINMAN" Samoylov  - story, quests, scripting, design
      Alexander "SAUR" Berezin  - lead artist, art design, modelling
      Sergey "ZOOMER" Bokarev   - dialogue, coordination, community
    Technical support: Pyran and Foxx.
    Full credits, including the dialogue writers, testers, narrator and
    musicians, are in CREDITS.md in the repository.

FIXED EDITION
    Foxx. Updated sfall and SF-Configurator, mod integration, and a long
    list of fixes to the original game. Posted here with his blessing.

THE OLDER ENGLISH BUILD
    Almost all of the English text came from an existing English build of
    Olympus. Whoever made that translation did most of this work, and they
    are not identified anywhere I could find. If you know who they are,
    tell me and they get credited.

ENGINE
    sfall - Timeslip, NovaRain, phobos2077 and contributors.
    High Resolution Patch, SF-Configurator, and the bundled mods.

FALLOUT 2
    Black Isle Studios / Interplay.

THE COMMUNITY
    No Mutants Allowed and the wider Fallout modding scene. And countless
    others.


Corrections to any credit here are welcome and will be applied verbatim.
"""


def find_7z():
    for c in SEVENZIP:
        if os.path.exists(c):
            return c
    found = shutil.which("7z")
    if found:
        return found
    raise RuntimeError("7-Zip not found")


def check_clean():
    """Refuse to build a release with Russian still in it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import re as _re
    import oly_tool as T
    from falloutloc import dat_replace as dr
    fe_raw, fe, _o, _ob = T.load_sides()
    bad = 0
    for name, e in fe.items():
        loose = os.path.join(T.FE, "data", name.replace("\\", os.sep))
        data = open(loose, "rb").read() if os.path.isfile(loose) else dr.content(fe_raw, e)
        bad += sum(1 for x in T.entries(data) if T.cyr(x[2]))
    print(f"  pre-flight: {bad} russian strings on disk")
    return bad == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--game", default=GAME)
    ap.add_argument("--skip-verify", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.game):
        print(f"game not found: {args.game}")
        return 1

    out = os.path.abspath(args.out)
    staging = os.path.join(out, "_staging", NAME)
    archive = os.path.join(out, NAME + ".zip")
    os.makedirs(out, exist_ok=True)
    if os.path.exists(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    if not args.skip_verify and not check_clean():
        print("russian still on disk -- refusing to build. run oly_tool.py verify")
        return 1

    print(f"staging {args.game}")
    t0 = time.time()
    cmd = ["robocopy", args.game, staging, "/E", "/MT:16", "/R:1", "/W:1",
           "/NFL", "/NDL", "/NJH", "/NJS", "/NP"]
    cmd += ["/XF"] + SKIP_FILES
    cmd += ["/XD"] + [os.path.join(args.game, d) for d in SKIP_DIRS]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode >= 8:
        print(f"robocopy failed ({r.returncode})")
        return 1

    with open(os.path.join(staging, "Play Olympus 2207.bat"),
              "w", newline="\r\n") as f:
        f.write(LAUNCHER.format(exe=EXE))
    with open(os.path.join(staging, "READ ME FIRST.txt"), "w", newline="\r\n") as f:
        f.write(READ_ME.format(exe=EXE))
    with open(os.path.join(staging, "CREDITS.txt"), "w", newline="\r\n") as f:
        f.write(CREDITS)

    size_raw = sum(os.path.getsize(os.path.join(b, n))
                   for b, _, fs in os.walk(staging) for n in fs)
    print(f"  staged {size_raw / 2**20:.0f} MB in {time.time() - t0:.0f}s")

    print("compressing")
    if os.path.exists(archive):
        os.remove(archive)
    t0 = time.time()
    r = subprocess.run([find_7z(), "a", "-tzip", "-mx=5", "-mmt=on", "-bso0", "-bsp0",
                        archive, staging], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"7z failed ({r.returncode})\n{r.stdout}\n{r.stderr}")
        return 1
    shutil.rmtree(os.path.join(out, "_staging"), ignore_errors=True)

    size = os.path.getsize(archive)
    print(f"  {size / 2**20:.0f} MB in {time.time() - t0:.0f}s "
          f"({100 * size / size_raw:.0f}% of raw)")
    if size > ASSET_LIMIT:
        print("  !! over GitHub's 2 GB asset limit")
        return 1
    print(f"\n{archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
