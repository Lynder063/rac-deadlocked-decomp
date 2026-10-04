# Ratchet: Deadlocked Decompilation

[![Progress report](https://github.com/Lynder063/rac-deadlocked-decomp/actions/workflows/progress.yml/badge.svg)](https://github.com/Lynder063/rac-deadlocked-decomp/actions/workflows/progress.yml)
[![Code](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp)
[![Functions](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://decomp.dev/Lynder063/rac-deadlocked-decomp)

A work-in-progress **matching decompilation** of *Ratchet: Deadlocked*
(*Ratchet: Gladiator* in PAL regions; Insomniac Games, 2005), NTSC-U version for the
PlayStation 2. The goal is C/C++ source that, built with the original
toolchain, produces a byte-identical copy of the retail executable.

The project runs in two phases:

1. **Match.** Write source that compiles to exactly the retail machine code.
   This is what proves a function has been understood: the compiler judges
   the result, not a read-through.
2. **Make it readable.** Refactor matched code toward idiomatic C++ with real
   names, types and structure. The matching build acts as the regression test
   for every cleanup.

> **Status: early.** The build pipeline exists and a growing number of functions
> match. Start with [`docs/RESEARCH.md`](docs/RESEARCH.md).

## Progress

Progress is tracked on [decomp.dev](https://decomp.dev/Lynder063/rac-deadlocked-decomp)
(once the repository is registered there).

| Version | Region | Game ID | Code | Functions |
|---|---|---|---|---|
| v1.00 | NTSC-U (`VER = 1.00`) | `SCUS_974.65` | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp) | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&label=Functions&measure=matched_functions)](https://decomp.dev/Lynder063/rac-deadlocked-decomp) |

Only NTSC-U is targeted. PAL (*Ratchet: Gladiator*) may follow as a second
version if someone with a PAL disc joins.

| Category | Progress | Contents |
|---|---|---|
| Game | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=game&label=Game&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=game) | All decompiled game code |
| Core | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=core&label=Core&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=core) | Engine and SDK code that stays resident (`core.text`) |
| Network | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=net&label=Network&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=net) | Network code (`net.text`) |
| libgcc | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=libgcc&label=libgcc&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=libgcc) | GCC runtime library rebuilt from GCC's own source (`src/libgcc/`) |
| Level code | [![](https://decomp.dev/Lynder063/rac-deadlocked-decomp.svg?mode=shield&category=level&label=Level%20code&measure=matched_code_percent)](https://decomp.dev/Lynder063/rac-deadlocked-decomp/SCUS_974.65?category=level) | Level code (`.text`, overwritten per level) |

A function counts as matched when its compiled code equals retail with
relocatable fields masked (`tools/audit_matches.py`); this is not yet a
link-time comparison.

## Disclaimer

This repository contains **no game assets, executable, or disassembly**. To
build it you need your own legally obtained copy of the game. Read
[`LEGAL.md`](LEGAL.md) before contributing.

## Building

Not possible yet: the compiler has not been identified and the splat
configuration does not exist. The plan follows
[rac1-decomp](https://github.com/Lynder063/rac1-decomp): SN Systems ProDG
`ee-gcc` (32-bit Windows programs, run natively or through Wine in a
container), `splat` for the disassembly, `objdiff`-format reports for
decomp.dev.

### 1. Add your executable

Copy the main executable from your disc to `baserom/` (it is ignored by git).
From a disc image, `7z e game.iso SCUS_974.65 -obaserom` extracts it. The
expected SHA-1 is:

```
aa91b1c3b9b1a244320c47580b77342ef9856e95
```

### 2. Generate the disassembly

```
bash tools/setup_asm.sh
```

The retail executable is only a loader with a compressed game image
(`docs/RESEARCH.md`). The script checks the SHA-1, unpacks the image
(`tools/unpack_wad.py`), rebuilds an ELF from its sections
(`tools/split_image.py`) and runs [splat](https://github.com/ethteck/splat)
with `config/splat.yaml` into `asm/` (not tracked in git). It creates a
`venv/` with the pinned versions from `requirements.txt` on first use.

### 3. Get the toolchain

The compilers are third-party mirrors of commercial software and are not part
of this repository. The current best candidate is **SN GCC 2.95.3 v1.36**
(`ee-gcc2953.exe`) with `-O2 -G8 -fopt-stack -mno-check-zero-division`,
found in the ProDG 3.01 mirror:

```
git clone https://github.com/AngheloAlf/SN-Systems-ProDG_for_PS2_3.01 toolchain/sn-prodg-3.01
git clone https://github.com/AngheloAlf/sce_ps2_sdk_24 toolchain/sn-prodg-24
```

On Linux and macOS the 32-bit Windows programs run through Wine in a
container: `bash tools/docker/run.sh <command>`. See
[`docs/RESEARCH.md`](docs/RESEARCH.md) ("Compiler search") for how the
compiler was identified and what is still open. 
### 4. Build and check

```
bash tools/docker/run.sh bash tools/build.sh      # compiles src/ with SN GCC 2.95.3 v1.36 -O2 -G8 -fopt-stack
bash tools/docker/run.sh bash tools/build_libgcc.sh   # libgcc with Sony's 2.9-ee
venv/bin/python tools/audit_matches.py            # compares each function with retail
python tools/gen_progress_report.py               # progress/report.json for decomp.dev
```

There is no linked image yet, so matching is checked function by function.

## Project structure

| Path | Contents |
|---|---|
| `src/core/` | Engine and SDK code, named by start address until the real source file is known |
| `src/game/` | Game code, one file per original source file where known |
| `src/libgcc/` | GCC's `libgcc2.c` and `fp-bit.c` (GPL with the libgcc exception), see its README |
| `include/` | Shared headers, recovered structs, assembly macros |
| `config/` | splat configuration, symbol maps, link order (to be added) |
| `tools/` | Build, audit and progress-report scripts; `unpack_wad.py` and `split_image.py` turn the retail executable into an ELF |
| `tools/docker/` | Build container (to be added) |
| `docs/` | Research, workflow and toolchain notes |
| `notes/` | Working notes and investigations |
| `baserom/` | Your own executable, not tracked |
| `asm/` | Locally generated disassembly, not tracked |
| `progress/report.json` | objdiff-format progress report read by decomp.dev |

### decomp.dev

[`.github/workflows/progress.yml`](.github/workflows/progress.yml) validates
`progress/report.json` and uploads it as the artifact `SCUS_974.65_report`.
Register the repository once at <https://decomp.dev/manage/new>. The report
is generated locally by `python tools/gen_progress_report.py` and committed
with each change, because CI cannot build the game.

## Resources

- [decomp.wiki](https://decomp.wiki): matching-decompilation knowledge base
- [decomp.dev](https://decomp.dev): progress tracking
- [OpenRAC](https://github.com/OpenRAC/OpenRAC): umbrella for the PS2 Ratchet & Clank decomps
- [rac1-decomp](https://github.com/Lynder063/rac1-decomp): the first game; this repo's structure and workflow come from it
- [ratchet-uya-decomp](https://github.com/vetusmagnus/ratchet-uya-decomp): Up Your Arsenal, the closest engine relative
- [splat](https://github.com/ethteck/splat),
  [spimdisasm](https://github.com/Decompollaborate/spimdisasm),
  [m2c](https://github.com/matt-kempster/m2c),
  [asm-differ](https://github.com/simonlindholm/asm-differ),
  [objdiff](https://github.com/encounter/objdiff)

## Credits

Full list with what each was used for: [`docs/CREDITS.md`](docs/CREDITS.md).

- **GFI (Game Fuckery Inc.)**: Special thanks to the GFI Discord server for the years of time spent researching and exploring these games, which helped make this decompilation possible.
- [rac1-decomp](https://github.com/Lynder063/rac1-decomp): project layout, workflow and toolchain research.
- [OpenRAC](https://github.com/OpenRAC/OpenRAC) and [ratchet-uya-decomp](https://github.com/vetusmagnus/ratchet-uya-decomp): sibling decompilations of the same engine family.
- [AngheloAlf](https://github.com/AngheloAlf): PS2 toolchain mirrors.
- [splat](https://github.com/ethteck/splat), [spimdisasm](https://github.com/Decompollaborate/spimdisasm), [m2c](https://github.com/matt-kempster/m2c), [asm-differ](https://github.com/simonlindholm/asm-differ), [objdiff](https://github.com/encounter/objdiff) and [decomp.dev](https://decomp.dev).
