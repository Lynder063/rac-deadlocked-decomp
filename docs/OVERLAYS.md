# Level overlays

Every level of the game carries its own build of the level code: an overlay
loaded over the resident image when the level starts. This page describes what
the overlays are, how they are split here, and how they are counted. It is
the same arrangement as in
[rac1-decomp](https://github.com/Lynder063/rac1-decomp)'s `docs/OVERLAYS.md`.

## What an overlay is

The resident image (`SCUS_974.65`, see `docs/RESEARCH.md`) holds `.vutext`,
`core.*` and `net.text`, which stay in memory, and also the sections `.lit`,
`.bss`, `.data`, `lvl.vtbl`, `lvl.camvtbl`, `lvl.sndvtbl` and `.text`. The
last group is overwritten when a level loads: each level has its own copy,
stored on the disc in the level's files in the format documented by the wrench
project (`docs/file_loading.md`: a stream of 16-byte section headers, each
followed by its data). The code in the resident `.text` is the code of the
first stage (the menus): 97 percent of it is contained in the multiplayer menu
overlay.

There are **47 overlays**: 24 campaign levels and 23 multiplayer levels, with
split-screen variants. Their `.text` is 2.6 to 3.1 MB each and starts at a
different address in each (`0x3A1580` to `0x4EEF00`), so functions are
identified by their code, not by their address.

## Getting them

The overlays are not in the executable. Unpack your disc image with the wrench
build tool, which writes one `overlay.elf` per level:

```
wrenchbuild unpack GAME.iso -o DIR -g dl -r us       # levels/*/*/overlay.elf
venv/bin/python tools/split_overlays.py DIR
```

`DIR` is a private folder (about 5 GB for the whole disc); nothing from it is
committed.

## How they are split (`tools/split_overlays.py`)

1. The `.text` of each overlay is cut into functions: the section start, every
   `jal` target inside it, and the instruction after a `jr $ra` and its delay
   slot (the same rule as `tools/find_functions.py`).
2. Each function is hashed by its normalised code (`tools/retail.py`: jump
   targets and relocatable immediates masked), so the same function in two levels
   is the same function whatever its address.
3. Every distinct function gets a class:

| Class | Meaning | Where it is counted |
|---|---|---|
| `main` | identical to a function of the resident `.text` | with the resident level text (not counted twice) |
| `common` | in two or more overlays | once, in category **Common** |
| `level` | in exactly one overlay | once, in **Level-specific** and in that level's own category |

Output, committed (names, addresses and sizes only):

- `config/overlays.tsv`: one row per overlay (id, directory, `.text` address and size);
- `config/overlay_functions.tsv`: one row per distinct function, named
  `func_L<level>_<address>` after the first overlay it occurs in.

## What is in them

| Class | Distinct functions | Code |
|---|---|---|
| `main` (already in the resident text) | 3,869 | 1,228 KB |
| `common` | 4,714 | 2,542 KB |
| `level` | 2,315 | 812 KB |

4,161 functions (1.5 MB) are in all 47 overlays; most of the rest are shared by
the 24 campaign levels or by the multiplayer levels. The only code that belongs
to a single level is the multiplayer menu's (`L00`); the other 46 overlays
consist of common code only.

**Progress per level.** The report has a category `level_NN` for each of the 47
levels. Common functions are grouped by the exact set of levels that contain
them (213 groups, one report unit each) and every unit is tagged with all the
levels in its set, so a level's category adds up all the overlay code that
level has, shared or not. Overlay code identical to a resident function is not
included (it is counted in the resident level text). This is what the per-level
table in the README shows.

| Id | Level | Kind | `.text` at | `.text` size | Functions | Code |
|---|---|---|---|---|---|---|
| L00 | Multiplayer Menu | multiplayer | `0x004EEF00` | `0x28F220` | 7009 | 2475 KB |
| L01 | Dreadzone Station | campaign | `0x003C7C80` | `0x2FEA50` | 6837 | 2952 KB |
| L02 | Catacrom Graveyard | campaign | `0x003BFF80` | `0x2B66D0` | 6325 | 2679 KB |
| L04 | Sarathos Swamp | campaign | `0x003BF200` | `0x2B7498` | 6301 | 2682 KB |
| L05 | Dark Cathedral | campaign | `0x003C1780` | `0x2DB6E8` | 6580 | 2822 KB |
| L06 | Temple Of Shaar | campaign | `0x003BEF00` | `0x2AFDE0` | 6332 | 2651 KB |
| L07 | Valix Lighthouse | campaign | `0x003BF300` | `0x2A29C8` | 6183 | 2603 KB |
| L08 | Mining Facility | campaign | `0x003BF200` | `0x2BA998` | 6393 | 2695 KB |
| L10 | Torval Ruins | campaign | `0x003C0580` | `0x2C3970` | 6426 | 2726 KB |
| L11 | Tempus Station | campaign | `0x003BE500` | `0x2B2C50` | 6279 | 2665 KB |
| L13 | Maraxus Prison | campaign | `0x003C0500` | `0x2CA518` | 6473 | 2751 KB |
| L14 | Ghost Station | campaign | `0x003C0A00` | `0x2C3968` | 6407 | 2729 KB |
| L15 | Control Level | campaign | `0x003C4C00` | `0x2CFC40` | 6465 | 2776 KB |
| L21 | Dreadzone Station Splitscreen | campaign | `0x003C7C80` | `0x2FEA50` | 6837 | 2952 KB |
| L22 | Catacrom Graveyard Splitscreen | campaign | `0x003BFF80` | `0x2B66D0` | 6325 | 2679 KB |
| L24 | Sarathos Swamp Splitscreen | campaign | `0x003BF200` | `0x2B7498` | 6301 | 2682 KB |
| L25 | Dark Cathedral Splitscreen | campaign | `0x003C1780` | `0x2DB6E8` | 6580 | 2822 KB |
| L26 | Temple Of Shaar Splitscreen | campaign | `0x003BEF00` | `0x2AFDE0` | 6332 | 2651 KB |
| L27 | Valix Lighthouse Splitscreen | campaign | `0x003BF300` | `0x2A29C8` | 6183 | 2603 KB |
| L28 | Mining Facility Splitscreen | campaign | `0x003BF200` | `0x2BA998` | 6393 | 2695 KB |
| L30 | Torval Ruins Splitscreen | campaign | `0x003C0580` | `0x2C3970` | 6426 | 2726 KB |
| L31 | Tempus Station Splitscreen | campaign | `0x003BE500` | `0x2B2C50` | 6279 | 2665 KB |
| L33 | Maraxus Prison Splitscreen | campaign | `0x003C0500` | `0x2CA518` | 6473 | 2751 KB |
| L34 | Ghost Station Splitscreen | campaign | `0x003C0A00` | `0x2C3968` | 6407 | 2729 KB |
| L35 | Control Level Splitscreen | campaign | `0x003C4C00` | `0x2CFC40` | 6465 | 2776 KB |
| L41 | Battledome Tower | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L42 | Catacrom Graveyard | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L44 | Sarathos Swamp | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L45 | Dark Cathedral | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L46 | Temple Of Shaar | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L47 | Valix Lighthouse | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L48 | Mining Facility | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L50 | Torval Ruins | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L51 | Tempus Station | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L53 | Maraxus Prison | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L54 | Ghost Station | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L61 | Battledome Tower Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L62 | Catacrom Graveyard Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L64 | Sarathos Swamp Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L65 | Dark Cathedral Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L66 | Temple Of Shaar Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L67 | Valix Lighthouse Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L68 | Mining Facility Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L70 | Torval Ruins Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L71 | Tempus Station Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L73 | Maraxus Prison Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |
| L74 | Ghost Station Splitscreen | multiplayer | `0x003A1580` | `0x28DAA8` | 5885 | 2513 KB |

## Disassembly (`tools/gen_overlay_asm.py`)

```
OVERLAYS=DIR bash tools/setup_asm.sh          # or: venv/bin/python tools/gen_overlay_asm.py DIR
```

Every distinct function is disassembled once, in the overlay where it occurs
first (the level id in its name). For each of the 14 overlays that is first
for some function (`L00`, `L01`, `L02`, `L04` to `L08`, `L10`, `L11`, `L13`,
`L14`, `L15`, `L41`) the tool writes a splat configuration for its
`overlay.elf` (one segment per section), with the canonical function names
and boundaries from `config/overlay_functions.tsv`, plus the resident
functions as external symbols so calls into the core code are named. The
result is in `asm/overlays/<id>/nonmatchings/` (not tracked, 430 MB). Functions
that contain data (a `b` jumps over it) get a splat subsegment of their own,
as in the resident `.text` (`docs/RESEARCH.md`).

Result: **6,806 of 7,029** functions (every common and level-specific
function). All 13 overlays other than `L00` are complete. In `L00` (the menu)
223 small functions are merged into the function before them, because splat
runs on past a function's declared size; they are not yet in separate files.

## Decompiling overlay functions

An overlay function is named `func_<level>_<address>` (for example
`func_L01_00631CB8`) and its source goes to `src/overlays/<level>/<ADDRESS>.c`,
where level and address are those in its name and in
`asm/overlays/<level>/nonmatchings/`. `tools/build.sh` compiles it like any other
file (same compiler, flags and assembler passes). `tools/audit_matches.py` and
`tools/diff_func.py` compare it with the bytes in that level's `overlay.elf`, found in
`$OVERLAYS` or `private/overlays` (a symlink to the folder from
`wrenchbuild unpack`). Jump targets and relocatable immediates are masked, so
the different load addresses of the levels do not matter, and a match counts in
**every** level that contains the function.

## Status

Splitting, counting, disassembly and auditing are done. Six functions of the
first level have been matched (common code), which already shows in 2 other
levels' rows too (`level_41` has two of them). Not done yet: per-level link
information (the data and bss layouts differ per level).
