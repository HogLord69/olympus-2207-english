# Payload — the non-`.msg` half of the localization

`oly_tool.py` handles dialogue and UI strings. This folder holds everything the
pipeline does not reach: artwork with text baked into the pixels, premade
character records, narration files, two mod folders, sfall's own `.ini`
messages, the handful of `.msg` files that had to be repaired by hand, and two
quest scripts with Fixed Edition bugs fixed.

The tree mirrors the game folder. Copy `payload/` over your install and the
engine picks it up — `ddraw.ini`'s load order puts loose files under `data/`
ahead of every archive.

```
data/premade/          9 files    character names and biographies
data/art/intrface/   126 files    interface art with English captions
data/art/inven/        1 file     dagnote.frm
data/pcx/             11 files    help screen and tip buttons
data/text/english/    63 files    narration, credits, screen names, repairs,
                                  intro subtitles
data/scripts/          2 files    Defender raid fixes (olxcchef, oln34)
data/art/cuts/         1 file     VSUIT.MVE, the "10 years later..." title card
sfall/                 2 files    translations.ini and the Key Mod script
mods/                  2 files    KeysHelp and InventoryFilter
```

## Premade characters

The Fixed Edition's `.gcd` files are byte-identical to the English build's apart
from the 32-byte name field at `0x174` (and eight trailing bytes), so only that
field was patched — no stat or format change. **Chris**, **Cliff** and **Kevin**,
plus `none` on the blank, demo and player templates. The three `.bio` files are
the English build's verbatim.

Left alone deliberately: FE's `blank`, `demo` and `player` GCDs carry EMP
resistance 0 where the English ones have 100. That is a pre-existing gameplay
difference in the Fixed Edition, not a translation problem.

## Interface art

All 123 `art/intrface` files that differ between the two builds turned out to be
the same image with localised text baked in. Every one was verified by rendering
both and diffing the changed pixel regions — not by trusting a hash.

Two differences were left as the Fixed Edition's on purpose:

- **`hr_mainmenu.frm`** — FE redrew the main menu and it is already English. The
  English build ships the older v1.2 art with the flag, so overwriting would
  have been a downgrade.
- **`bl308new.frm`** — art-only difference, no text in it.

`art/intrface` now matches the English build on **497 of 499** files, both
exceptions intentional.

### Russian UI with no English source

Some screens had no English original to copy, because the Fixed Edition built
them itself:

- `sfall.dat`'s `INVBOX2` / `LOOT2` (expanded inventory, `ExpandInventory=1`) and
  `WORLDMAP` / `WORLDMAP_WIDE` (`ExpandWorldMap=1`, `WideWorldMap=1`) are FE-built
  widened versions of the 640×480 screens. The column mapping was recovered and
  only pixels provably copied from the Russian art were repainted, so **ARMOR**,
  **ITEM 1**, **ITEM 2**, **DONE**, **TAKE ALL**, **TOWN** and **WORLD** read
  English. Headers and file sizes are byte-identical.
- `data/pcx/HELPSCRN.PCX` and ten tip buttons — НАЗАД, ЗАКРЫТЬ, ДА, НЕТ, ДАЛЕЕ
  became BACK, CLOSE, YES, NO, NEXT — copied from the English install.

## sfall's own messages

`sfall/translations.ini` is not a `.msg` file, so nothing in the pipeline ever
read it. It carries the karma messages, the save prompt, poison damage, the
barter cost label, the party HUD labels and the fourteen unarmed attack names.
It is fixed by copying Resurrection's English file, verified key-for-key first:
56 keys, six sections, identical order, and `XltTable` — the codepage map, the
one value that is not a message — byte-identical between them, so the copy
changes no behaviour.

Six symptoms reported against v1.1 all trace here and nowhere else: `ОЗ:` where
HP belongs, `Электро` on the armour class, `Вы теряете N ед. кармы`, the barter
`Стоимость`, `Сохранение в данный момент невозможно`, and
`Отдыхать двадцать четыре часа` on the Pip-Boy's 24-hour rest option.

`sfall/scripts/gl_key_mod.int` holds its two F3 messages hardcoded, so they are
space-padded to the original byte length like the Keys Help strings.

## Mods

Both are sfall folder-mods, despite the `.dat` names.

- **`KeysHelp.dat/scripts/gl_keyshelp.int`** (the J key) — its strings are
  hardcoded in the compiled script, so the English replacements are space-padded
  to the exact original byte length. File size is unchanged.
- **`InventoryFilter.dat/text/english/game/inventory_filter.msg`** — translated.

## Repaired `.msg` files

Eleven files here are not ports — they are repairs to files the pipeline already
produced, where a translation tool had re-wrapped or misnumbered a block.

**`PIPBOY.MSG`.** Its label section was re-wrapped to a fixed width, which
destroyed the line-number to text mapping. Holodisk titles 406–419 were gone
entirely and 400–405 held run-on text, so the Pip-Boy printed `Error` in the
DATA column instead of a holodisk name. Three stray duplicate entries per disk
made it worse: Fallout 2's loader lets a repeated id overwrite the earlier one,
so each disk's first line became the end-of-disk marker and every disk stopped
at line one. The whole sub-1000 block is restored from the English build — id
sets below 1000 are identical between the two, so nothing FE-specific is lost —
and the strays are dropped. All 13 holodisks now resolve: title present, body
contiguous, `**END-DISK**` terminated. The alarm clock, movie list and status
labels were damaged the same way and come back with it.

**Ten more** had their last block written with the wrong line numbers, which
both blanked the working lines and left the intended ids missing:

    COMBATAI  PERK  STTEXT  NWMARK  OLMORO  SJOSVALD  NWSAT  RBBELOCH
    TGRDDEAD  TIPTEXT

In `STTEXT.MSG` that silently replaced the guards' `It's the heretic! KILL HIM!`
with empty lines; in `NWMARK.MSG` three replies shadowed an earlier dialogue node
and 521–523 came back as `Error`. The translated lines were kept and renumbered
onto the ids they were written for — only two had no counterpart and were taken
from the English build.

Duplicate ids are not by themselves a defect: `OLKELLY`, `PRO_SCEN`, `TDUDEDAD`,
`TCAROL01`, `RBPASTUH` and `NWXBRST` carry them in both upstream builds too, and
are left alone.

## `dagnote.frm`

The "Note from Douglas" inventory picture, and a 15× size outlier — every other
inventory image is at most 200×69, this one is 300×322 in the Fixed Edition and
350×350 in the English build, and the interface bar scales whatever sits in the
active item slot. v1.1 shipped the English 350×350 and the item was then
reported as crashing the game when placed in a hand slot. The English artwork is
now inside FE's own 300×322 frame — trimmed of its transparent margin, scaled
uniformly, and centred — byte-for-byte the original file size. Unconfirmed as
the cause; it restores the only geometry this build shipped with.

## "10 years later..." title card

`data/art/cuts/VSUIT.MVE` is the short movie that plays a few missions in: a
black screen and one line of yellow text. The Fixed Edition's says
*10 ЛЕТ СПУСТЯ...*; this is the English 1.2 release's own movie, which says
*10 YEARS LATER...* in the same lettering.

It is the English release's file as shipped, not a re-encode. It runs 5 s
against the Fixed Edition's 4 s and its sound sting is quieter and at 48 kHz,
but the English release played it with the same `OLYMPUS.EXE`, and an MVE
declares its own audio format. `VSUIT.PAL` is identical in both builds, so only
the movie changes.

The patch overwrites the Fixed Edition's `VSUIT.MVE`, which lives loose in
`data/art/cuts/` rather than in an archive. Keep a copy if you want to revert.

## Defender raid scripts

`data/scripts/olxcchef.int` and `data/scripts/oln34.int` fix two bugs in the
Fixed Edition's Defender raid. Neither is a translation problem.

- **`olxcchef.int`, the Punisher squad leader.** Leaving the raid map ends the
  mission: every squad member starts a timer, the first to finish loads
  Olympus, and the engine cancels the rest on the map change. The soldiers have
  a per-update check that removes them from the party once global 336 says the
  raid is over. The leader had none, so he stayed in your party for good. He now
  runs the soldiers' exact check — five lines, copied from `olxcartl.int`.
- **`oln34.int`, Captain #34.** "Here's your Defender suit" created a new suit
  even if you already carried one. He now puts you in yours, and only creates
  one when you have none.

Full write-up, and the exact source change: [`../fixes/defender-raid.md`](../fixes/defender-raid.md).

## Intro subtitles

The intro is seven pages of the *Sacramento Chronicles* with the headlines
printed in Russian inside the video. `cuts/INTRO.SVE` puts one English subtitle
under each page — the headline, with its subheading where it fits — switched
halfway through each dissolve so the text always matches the page on screen.
The last page holds longer and gets two. Players need **Preferences →
Subtitles** switched on.

Wording follows the English 1.2 release's own intro, which carries the same
newspapers typeset in English, and uses the holodisk's terms for the two
invented states: РЕИ is the **UER**, ВША the **GSA**.

### How subtitles behave in this engine

Checked against fallout2-ce (`movie.cc`, `movie_lib.cc`) and sfall's HRP
(`HRP/MoviesScreen.cpp`):

- **A cue `N:text` fires on the N-th frame shown** — the counter is
  `rm_FrameCount`, incremented on MVE opcode `0x07`. This intro shows 1,020.
- **Playback waits one timer tick per frame shown.** The intro runs **42.5 s**
  at 24 fps, so each page is on screen for about 4 s. ffmpeg's timestamps for
  this file are inflated about six-fold (it counts container chunks), which is
  how the first version of these subtitles came to be timed as if the intro ran
  269 s: they landed on the right pages but lasted as little as 1.1 s each.
- **The subtitle box is one line tall.** Text is word-wrapped, but every line
  after the first is silently dropped. The wrap width is the screen width under
  sfall's HRP (1280 by default here) and 640 at native 640×480, so every cue is
  kept under 640 px in the game's font (`font1.aaf`, font 101; the widest is
  577 px).
- sfall's HRP shrinks the movie to leave a strip for the subtitle line and
  centres the line in it.

Each cue is up for 3.5–6.1 s at no more than 18 characters a second.

The English 1.2 intro was not swapped in: both play for about 42 s over the
identical soundtrack, but the English one is a lower-bitrate encode (97 MB
against 264 MB) and its frames decode here with visible block artifacts.

## Text

47 cutscene narration files, `credits.txt`, and `scrname.msg`. The Fixed Edition
had replaced `quotes.txt` with its own Russian build credits, so those were
translated rather than reverted to the stock Fallout 2 quotes.

### A bug in the English release, fixed here

The English build's `credits.txt` stores cp866 Cyrillic homoglyphs in place of
Latin letters — `0xE0`→p, `0xE3`→y, `0x8D`→H, `0x93`→Y. "Reynolds" was held as
`Re<г>nolds`. Under the Fixed Edition's fonts those render as Russian letters.
The same problem made the kid's scream in `SSXBOY.MSG` come out blank. Both are
remapped to ASCII, and `credits.txt` is now clean seven-bit throughout.
