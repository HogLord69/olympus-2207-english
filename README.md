# Olympus 2207 — English

English localization for **Olympus 2207 (Fixed Edition)**, Foxx's repack of the
Russian *Fallout 2* total conversion.

Download, unzip, double-click. Nothing to install, nothing to configure.

Grab a ready-to-play archive from **[Releases](../../releases)**, or apply the
patch to an install you already have with `oly_tool.py`.

**42,296 strings across 270 files. No Russian left.**

Plus the half that is not strings: **201 files** of interface art with English
text baked into the pixels, premade characters, narration, and two mod folders.
See [`payload/`](payload/).

---

## Most of this was a port, not a translation

An older English build of Olympus already existed. The Fixed Edition is the same
game, newer — so the English was already written for almost all of it.

| | Strings | How |
|---|---|---|
| Ported from the older English build | 35,603 | matched per string |
| Pip-Boy holodisks | 1,374 | re-flowed, see below |
| `ScrnSet.msg` (screen settings) | 76 | ported from `f2_res.dat` |
| Translated from scratch | 98 | content the FE added |

The 98 are in [`tr/t000.py`](tr/t000.py) — Ursul's weapon training, Doctor
Moreau's confrontation, a dozen combat barks, the Auto-Doc perk messages, and
the screen-settings help text.

## Install

Requires Python 3.8+.

```bash
python oly_tool.py survey
```

```bash
python oly_tool.py port
```

```bash
python pipboy_reflow.py
```

```bash
python port_scrnset.py
```

```bash
python oly_tool.py translate
```

```bash
python oly_tool.py verify
```

Output is loose files under `Olympus 2207 (FE)\data\text\english\`, which the
engine loads ahead of `master.dat` because `olympus.cfg` sets
`master_patches=data`. **No archive is ever rewritten.** Delete the loose files
to revert.

Paths are constants at the top of `oly_tool.py` — edit them if your installs
live elsewhere.

## Why porting per string, and not per file

Whole-file copying would silently drop what the Fixed Edition added: seven files
have different string-id counts between the two builds. Porting per string keeps
the FE's own structure and replaces only text, so new FE content survives as
Russian to be translated rather than vanishing.

**Id matching was verified before being relied on.** Across different games it
would be unsafe — every total conversion renumbers. These are two builds of one
game, and three independent checks agree:

- the audio field, which is language-independent, matches on 6,466 of 6,468
  shared ids (99.97%)
- strings already English on both sides agree where they overlap
- Russian and English lengths correlate at r ≥ 0.55 for 248 of 252 files, most
  near 0.99

The four low-correlation files were checked by hand and are correct — short
uniform strings like `Вы видите: ` → `You see a ` have no length variance to
correlate.

## The Pip-Boy needed re-flowing, not porting

Holodisks are pre-wrapped: one screen line per string id, pane about 51
characters. The FE re-wrapped them for Russian, which runs longer, so the builds
break lines in different places — 1,639 ids against 1,627, drifting by two or
more inside a disk.

Porting those by id pastes English onto the wrong lines. It scrambled every disk
on the first attempt: FE id 3096 is *"March 7, 2012"* while old id 3096 is
*"the START-II agreement"*.

[`pipboy_reflow.py`](pipboy_reflow.py) rebuilds the file instead. Disks pair by
thousand-block, confirmed by digit fingerprint — numbers survive translation, so
`3 марта 2151` and `March 3, 2151` share `3` and `2151`. The FE's marker order is
kept, the old build's English is re-wrapped to the pane, and a leading date stays
on its own line. A disk that needs more lines than the FE reserved simply gets
more ids; each block has 700–990 spare.

Pairing by id, by position, and by digits alone were all tried first and all
fail. The script reports a disagreement rather than guessing past it.

## Verifying

```bash
python oly_tool.py verify
```

Reads every `.msg` the way the engine will — loose file ahead of the archive —
and reports any Russian left. This is the check that counts: an installer
reporting what it wrote tells you nothing about what it didn't.

## Traps

1. **`.msg` is `{id}{}{text}`**, not `id=text`. An installer written for
   `id=text` matches nothing and reports success.
2. **Repeated string ids.** 19 files carry the same id twice with different
   lines. Reading a `.msg` into a dict keyed by id drops all but the last —
   which is how the first Pip-Boy attempt doubled the file and how ten barks
   survived a "100% complete" build on a sibling project. Everything here works
   on occurrence lists.
3. **`ScrnSet.msg` lives outside `master.dat`**, in `f2_res.dat` and
   `sfall.dat`. The `sfall` copy is the superset.
4. **Encode output as cp1251.** English is ASCII so it is lossless, but the
   surrounding file is cp1251 and byte-level patching must not disturb it.
5. **Do not rebuild `master.dat`.** Loose files under `data/` are the supported
   override path.

## Layout

```
oly_tool.py         survey / port / translate / verify / remaining
pipboy_reflow.py    holodisk re-flow
port_scrnset.py     the screen-settings UI, which sits outside master.dat
tr/t000.py          the 98 hand translations, keyed by russian text
```

## Licence and credit

Tooling and English text: MIT, see [LICENSE](LICENSE). Take it, pass it on.

Olympus 2207 belongs to its authors — see [CREDITS.md](CREDITS.md). Credit them.
