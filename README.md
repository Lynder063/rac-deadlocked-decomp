# Ratchet: Deadlocked Decompilation

[![Progress report](https://github.com/Lynder063/rac-deadlocked-decomp/actions/workflows/progress.yml/badge.svg)](https://github.com/Lynder063/rac-deadlocked-decomp/actions/workflows/progress.yml)
[![Code](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp)
[![Functions](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://decomp.dev/Lynder063/rac-deadlocked-decomp)

A work-in-progress **matching decompilation** of *Ratchet: Deadlocked*
(*Ratchet: Gladiator* in PAL regions; Insomniac Games, 2005) for the
PlayStation 2, NTSC-U version. The goal is C/C++ source that, built with the
original toolchain, produces a byte-identical copy of the retail executable.

The project runs in two phases:

1. **Match.** Write source that compiles to exactly the retail machine code.
   This is what proves a function has been understood: the compiler judges
   the result, not a read-through.
2. **Make it readable.** Refactor matched code toward idiomatic C++ with real
   names, types and structure. The matching build acts as the regression test
   for every cleanup.

> **Status: early.** The whole build pipeline works (unpacking the retail
> image, disassembly, compiler and flags identified, library code rebuilt from
> its open-source originals) and functions are matching. There is no linked
> image yet, so matching is checked function by function.

## Progress

Progress is tracked on [decomp.dev](https://decomp.dev/Lynder063/rac-deadlocked-decomp).

| Version | Region | Game ID | Code | Functions |
|---|---|---|---|---|
| v1.00 | NTSC-U (`VER = 1.00`) | `SCUS_974.65` | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp) | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://decomp.dev/Lynder063/rac-deadlocked-decomp) |

Only NTSC-U is targeted. PAL (*Ratchet: Gladiator*) may follow as a second
version if someone with a PAL disc joins.

| Category | Progress | Contents |
|---|---|---|
| Game | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=game&label=Game&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=game) | All game code |
| Core | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=core&label=Core&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=core) | Engine and SDK code that stays resident (`core.text`) |
| Network | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=net&label=Network&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=net) | Network code (`net.text`) |
| Resident level code | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=level&label=Resident%20level%20code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=level) | The level text kept in the executable (`.text`); the menus' code |
| libgcc | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=libgcc&label=libgcc&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=libgcc) | GCC runtime library rebuilt from GCC's own source (`src/libgcc/`) |
| libm | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=libm&label=libm&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=libm) | Math library rebuilt from newlib's source (`src/libm/`) |
| Level overlays | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=overlays&label=Level%20overlays&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=overlays) | All level overlay code (`docs/OVERLAYS.md`) |
| Common | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=common&label=Common&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=common) | Overlay code shared by two or more levels |
| Level-specific | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=levels&label=Level-specific&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=levels) | Overlay code found in one level only (the multiplayer menu) |

### Level overlays

Each level carries its own build of the level code, loaded over the resident
image when the level starts ([`docs/OVERLAYS.md`](docs/OVERLAYS.md)). There are
47 overlays (24 campaign and 23 multiplayer levels) that share 85 to 97 percent of
their code at different addresses. Their functions are split and counted once
each: code shared by two or more levels under *Common* (4,714 functions),
code found in one level only under *Level-specific* (2,315 functions, all of
them the multiplayer menu's) and that level's own row. Functions identical to
one in the resident level text are counted there, not twice. The overlays
come from your own disc: unpack it with the
[wrench](https://github.com/chaoticgd/wrench) build tool and run
`tools/split_overlays.py` (see `docs/OVERLAYS.md`). Nothing is decompiled in
them yet.

A function counts as matched when its compiled code equals retail with
relocatable fields masked (`tools/audit_matches.py`). This is not a
link-time comparison yet, so a function that calls or reads the wrong symbol
can still count.

## Disclaimer

This repository contains **no game assets, executable, or disassembly**. To
build it you need your own legally obtained copy of the game. Read
[`LEGAL.md`](LEGAL.md) before contributing.

## How it works

- **The executable is a loader plus a packed image.** `tools/unpack_wad.py`
  decodes the compressed game image and `tools/split_image.py` splits it into
  its 17 sections and rebuilds an ELF for [splat](https://github.com/ethteck/splat)
  (`docs/RESEARCH.md`).
- **The compiler is SN GCC 2.95.3 v1.36** with
  `-O2 -G8 -fopt-stack -mno-check-zero-division`, run as 32-bit Windows
  programs (through Wine in a container on Linux and macOS). Retail was
  assembled by SN's own assembler, whose nops and constant sequences
  `tools/cc.sh` reproduces.
- **Level code is overlays.** Each level has its own copy of the level code,
  47 in all, split by `tools/split_overlays.py` into common and level-specific
  functions, as in rac1-decomp (`docs/OVERLAYS.md`).
- **Library code is rebuilt from source.** libgcc comes from GCC and libm from
  newlib, both built unchanged with Sony's `2.9-ee` driver and matched against the
  retail bytes; only files that match are kept.

## Quick start

```
git clone git@github.com:Lynder063/rac-deadlocked-decomp.git
cd rac-deadlocked-decomp
cp /path/to/SCUS_974.65 baserom/                 # SHA-1 aa91b1c3b9b1a244320c47580b77342ef9856e95
bash tools/setup_asm.sh                           # unpack, split, splat -> asm/
git clone https://github.com/AngheloAlf/SN-Systems-ProDG_for_PS2_3.01 toolchain/sn-prodg-3.01
git clone https://github.com/AngheloAlf/sce_ps2_sdk_24 toolchain/sn-prodg-24
bash tools/docker/run.sh bash tools/build.sh      # compile src/
venv/bin/python tools/audit_matches.py            # compare every function with retail
python3 tools/gen_progress_report.py              # progress/report.json for decomp.dev
```

The compilers are third-party mirrors of commercial software and are not part
of this repository. [`CONTRIBUTING.md`](CONTRIBUTING.md) has the full setup,
how code is compiled, how to add a function and what tends to make functions
match.

## Project structure

| Path | Contents |
|---|---|
| `src/core/`, `src/net/`, `src/game/` | Decompiled game code, one file per start address until the real source file is known |
| `src/libgcc/`, `src/libm/` | GCC's runtime library and newlib's math library, sources that match retail (see their READMEs and `THIRD_PARTY_NOTICES.md`) |
| `include/` | Shared headers (`common.h`) and assembly macros |
| `config/` | splat configuration, section table, function list (`functions.tsv`), library tables (`libgcc.tsv`, `libm.tsv`) and the level overlays (`overlays.tsv`, `overlay_functions.tsv`) |
| `tools/` | Unpacker, section splitter, compile pipeline (`cc.sh`), audit, diff and report tools |
| `tools/docker/` | The build container runner |
| `nonmatching/` | Drafts that do not match yet (not built) |
| `docs/` | `RESEARCH.md` (how the executable is built and rebuilt), `OVERLAYS.md` (the level overlays), `CREDITS.md` |
| `baserom/` | Your own executable, not tracked |
| `asm/` | Locally generated disassembly, not tracked |
| `progress/report.json` | objdiff-format progress report read by decomp.dev |

### decomp.dev

[`.github/workflows/progress.yml`](.github/workflows/progress.yml) validates
`progress/report.json` and uploads it as the artifact `SCUS_974.65_report`. The
report is generated locally by `python3 tools/gen_progress_report.py` and
committed with each change, because CI cannot build the game (the compiler and
the executable cannot be redistributed). CI fails if the report disagrees with
`src/`.

## Contributing

Contributions are welcome: see [`CONTRIBUTING.md`](CONTRIBUTING.md). A good first
step is a small function from `asm/nonmatchings/`, a draft from `m2c`, and
`tools/diff_func.py` to compare it with retail.

## Resources

- [decomp.wiki](https://decomp.wiki): matching-decompilation knowledge base
- [decomp.dev](https://decomp.dev): progress tracking
- [OpenRAC](https://github.com/OpenRAC/OpenRAC): umbrella for the PS2 Ratchet & Clank decomps
- [rac1-decomp](https://github.com/Lynder063/rac1-decomp): the first game; this repo's structure and workflow come from it
- [ratchet-uya-decomp](https://github.com/vetusmagnus/ratchet-uya-decomp): Up Your Arsenal, the closest engine relative
- [wrench](https://github.com/chaoticgd/wrench): toolkit and documentation for the PS2 Ratchet & Clank file formats
- [splat](https://github.com/ethteck/splat),
  [spimdisasm](https://github.com/Decompollaborate/spimdisasm),
  [m2c](https://github.com/matt-kempster/m2c),
  [asm-differ](https://github.com/simonlindholm/asm-differ),
  [objdiff](https://github.com/encounter/objdiff)

## Credits

Full list with what each was used for: [`docs/CREDITS.md`](docs/CREDITS.md).

- **GFI (Game Fuckery Inc.)**: Special thanks to the GFI Discord server for the years of time spent researching and exploring these games, which helped make this decompilation possible.
- [rac1-decomp](https://github.com/Lynder063/rac1-decomp): project layout, workflow, toolchain research, and the assembler passes.
- [ratchet-uya-decomp](https://github.com/vetusmagnus/ratchet-uya-decomp): compiler flags (`-fopt-stack`, `-G8`) and global-declaration findings.
- [OpenRAC](https://github.com/OpenRAC/OpenRAC): sibling decompilations of the same engine family.
- [wrench](https://github.com/chaoticgd/wrench): documentation of the packed image format and the executable's layout.
- [GCC](https://gcc.gnu.org) and [newlib](https://sourceware.org/newlib/): the library sources in `src/libgcc/` and `src/libm/`.
- [AngheloAlf](https://github.com/AngheloAlf): PS2 toolchain mirrors.
- [splat](https://github.com/ethteck/splat), [spimdisasm](https://github.com/Decompollaborate/spimdisasm), [m2c](https://github.com/matt-kempster/m2c), [asm-differ](https://github.com/simonlindholm/asm-differ), [objdiff](https://github.com/encounter/objdiff) and [decomp.dev](https://decomp.dev).

## License

The original work in this repository is MIT licensed (`LICENSE`). Files under
`src/libgcc/` and `src/libm/` keep their own licenses, stated in their headers
(GPL with the libgcc exception, and the Sun/fdlibm notice).
