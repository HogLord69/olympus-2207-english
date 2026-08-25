# Payload — the non-`.msg` half of the localization

`oly_tool.py` handles dialogue and UI strings. This folder holds everything that
is **not** a `.msg` string: artwork with text baked into the pixels, premade
character records, narration files, and two mod folders.

The tree mirrors the game folder. Copy `payload/` over your install and the
engine picks it up — `ddraw.ini`'s load order puts loose files under `data/`
ahead of every archive.

```
data/premade/          9 files    character names and biographies
data/art/intrface/   126 files    interface art with English captions
data/art/inven/        1 file     dagnote.frm
data/pcx/             11 files    help screen and tip buttons
data/text/english/    51 files    narration, credits, screen names
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

## Mods

Both are sfall folder-mods, despite the `.dat` names.

- **`KeysHelp.dat/scripts/gl_keyshelp.int`** (the J key) — its strings are
  hardcoded in the compiled script, so the English replacements are space-padded
  to the exact original byte length. File size is unchanged.
- **`InventoryFilter.dat/text/english/game/inventory_filter.msg`** — translated.

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
