# Contributing

This is a **matching decompilation** of *Ratchet: Deadlocked* (NTSC-U,
`SCUS_974.65`): C that, built with the original compiler, produces the same
machine code as the retail executable, function by function. This guide gets you
from a fresh clone to a working build and explains how to add a function.

Read [`LEGAL.md`](LEGAL.md) first. In short: no game data, executable or
disassembly in the repository, nothing from Sony's SDK source, and every name in
`src/` is your own work.

## 1. What you need

- Your own copy of the game (NTSC-U). The repo contains nothing of it.
- Linux, macOS or Windows (Git Bash). On Linux and macOS the compiler runs under
  Wine inside a container (Podman or Docker). The image is pulled
  automatically on first use: `bash tools/docker/run.sh <command>` runs any
  command inside it.
- Python 3.10 or newer.

## 2. Setup

```
git clone git@github.com:Lynder063/rac-deadlocked-decomp.git
cd rac-deadlocked-decomp
```

**The executable.** Copy `SCUS_974.65` from your disc to `baserom/` (it is
ignored by git). Its SHA-1 must be:

```
aa91b1c3b9b1a244320c47580b77342ef9856e95
```

**The disassembly.**

```
bash tools/setup_asm.sh
```

The retail executable is only a loader with a compressed game image
(`docs/RESEARCH.md`). The script checks the hash, unpacks the image
(`tools/unpack_wad.py`), rebuilds an ELF from its 17 sections
(`tools/split_image.py`), and runs [splat](https://github.com/ethteck/splat)
with `config/splat.yaml` into `asm/` (not tracked). A `venv/` with the pinned
tool versions is created on first use. Afterwards you can regenerate
`config/functions.tsv` (every function with address and size) with
`venv/bin/python tools/gen_function_list.py` if the splat configuration changed.

**The toolchain.** The compilers are third-party mirrors of commercial software
and are not in the repository:

```
git clone https://github.com/AngheloAlf/SN-Systems-ProDG_for_PS2_3.01 toolchain/sn-prodg-3.01
git clone https://github.com/AngheloAlf/sce_ps2_sdk_24 toolchain/sn-prodg-24
```

**The level overlays** (optional; needed only to regenerate `config/overlays.tsv`
and `config/overlay_functions.tsv`, which are committed). Unpack your disc with
the [wrench](https://github.com/chaoticgd/wrench) build tool and split them:

```
wrenchbuild unpack GAME.iso -o DIR -g dl -r us
venv/bin/python tools/split_overlays.py DIR
```

See `docs/OVERLAYS.md`.

**Helper tools** (used by the workflow below, cloned locally, not vendored):

```
git clone https://github.com/matt-kempster/m2c tools/ext/m2c
git clone https://github.com/simonlindholm/asm-differ tools/ext/asm-differ
```

## 3. Building and checking

```
bash tools/docker/run.sh bash tools/build.sh      # game code in src/ -> build/obj/
bash tools/docker/run.sh bash tools/build_libgcc.sh
bash tools/get_newlib.sh                           # once: the math library headers
bash tools/docker/run.sh bash tools/build_libm.sh
venv/bin/python tools/audit_matches.py             # compare every function with retail
python3 tools/gen_progress_report.py               # progress/report.json
python3 tools/gen_progress_report.py --check       # what CI runs
```

`tools/audit_matches.py` compares each compiled function with the retail bytes at
its address, with relocatable fields masked (jump targets, the immediate of
`lui`, and of loads, stores and adds that are not stack-relative). This is
**not** a link-time comparison: a function that calls or reads the wrong symbol
can still pass, so check calls and globals by eye.

### How code is compiled (`tools/cc.sh`)

Retail was built with **SN GCC 2.95.3 v1.36** (`ee-gcc2953.exe`), flags
`-O2 -G8 -fopt-stack -mno-check-zero-division`, then assembled by SN's own
assembler. Because that assembler is not usable here, `tools/cc.sh` reproduces
what it does:

1. compile to assembly (`-S`);
2. `tools/ps2eeas_dli.py`: expand 64-bit constants the way SN's assembler does;
3. assemble once with the compiler driver's GNU `as`;
4. `tools/ps2eeas_nops.py`: add the nops SN's assembler adds (it pads short
   loops, and puts a nop after an `mtc1` whose result is read next, and between
   a float compare and its `bc1`);
5. assemble again.

A source file can add compiler flags on its first line:

```c
/* cflags: -mno-split-addresses */
```

Use it for functions whose global accesses retail expands as one macro
(`lui $a0, hi; lw $a0, lo($a0)`, destination register as temporary).

### libgcc and libm

These are not game code. libgcc is GCC's `libgcc2.c`/`fp-bit.c`; libm is newlib's
math library (fdlibm). Both are built unchanged with Sony's `2.9-ee` driver
(`tools/build_libgcc.sh`, `tools/build_libm.sh`), and each compiled function is
paired with its retail address in `config/libgcc.tsv` and `config/libm.tsv`.
Only source files that match are kept in `src/libgcc/` and `src/libm/`
(see their READMEs for what does not match yet).
`tools/map_archive.py ARCHIVE.a NAME` makes such a table from a library
archive in the toolchain mirror (the archive is a reference for names and
addresses only, never a substitute for source).

## 4. Adding a function

1. **Pick one.** Look in `asm/nonmatchings/<segment>/func_XXXXXXXX.s`. Small
   functions without data tables are a good start. `config/functions.tsv` lists
   all of them with sizes.
2. **Get a starting point** with `venv/bin/python tools/ext/m2c/m2c.py -t
   mipsee-gcc-c asm/nonmatchings/.../func_XXXXXXXX.s`. The output is a draft: it
   usually needs types, struct members and cleaner control flow.
3. **Put it in `src/`** as `src/core/<ADDR>.c` (core text, below `0x163B80`),
   `src/net/<ADDR>.c` (network text, from `0x1E00000`) or `src/game/<ADDR>.c`
   (level text), defining `func_XXXXXXXX` (the address from `asm/`). A file may
   hold several functions. Start the file with `#include "common.h"`.
4. **Iterate.**
   `bash tools/docker/run.sh bash tools/build.sh`, then
   `venv/bin/python tools/diff_func.py func_XXXXXXXX` shows your function next to
   retail, word by word. `tools/try_variants.py` compiles several source forms of
   one function in a single run (see its docstring; `EXTRA="..."` passes flags).
5. **When it matches**, rerun `tools/audit_matches.py`, then
   `python3 tools/gen_progress_report.py` and commit the regenerated
   `progress/report.json` together with your source. CI fails if the report
   disagrees with `src/`.
6. **If it does not match yet**, keep it out of `src/` (put the draft in
   `nonmatching/<ADDR>.c` with a comment saying what differs). `nonmatching/` is
   not built.

### Things that make functions match

These came out of the work so far; add yours here.

- **Globals read with `lui`/`lw`** (not through `$gp`): declare them without a
  size so the compiler keeps them out of small data:
  ```c
  extern s32 D_00221ED8_[];
  #define D_00221ED8 (D_00221ED8_[0])
  ```
  and add `/* cflags: -mno-split-addresses */` if the destination register is the
  `lui` temporary in retail.
- **`-G8`**: variables of up to 8 bytes that retail reaches through `$gp` are
  plain `extern` declarations.
- **`volatile`**: a counter that retail reloads from memory, or a store that
  retail leaves a nop delay slot after, is usually `volatile`.
- **Array indexing**: `p = array + i` and `array[i].field` give different
  register orders; `*(T *)((u32)p + (i << 2))` differs again. Try them all.
- **Return values**: `return x == -1 ? 0 : x;` often matches where a temporary
  holding `~x` does not.
- **Parameter types**: an `s8` compared with `-1` adds sign extensions retail does
  not have; use `s32`.
- **Calls with unknown arguments**: a decompiler may pass a leftover register as
  an argument; if retail does not set it, declare the callee without parameters.
- **Not your fault**: a nop after `mtc1` or a loop padded to a minimum length
  is added by `tools/cc.sh`; if it is missing or extra for one function, the rule
  in `tools/ps2eeas_nops.py` needs refining, not the C.

### Level overlay functions

Functions of the level overlays (`func_L01_00631CB8` and so on) go to
`src/overlays/<level>/<ADDRESS>.c` and are checked against the level's `overlay.elf`;
see `docs/OVERLAYS.md` for how to get them and how they are counted.

### Automatic drafts (`tools/auto_structs.py`)

For small functions, `venv/bin/python tools/auto_structs.py prepare overlay N`
runs m2c, builds structures from the `->unkXX` accesses (members named by
offset, types from how they are used) and writes four compile variants;
`bash tools/docker/run.sh bash build/auto3/compile.sh` compiles them, `check`
keeps the ones that equal retail and `adopt` copies them into `src/`. The first
run matched 71 of 1,800 functions tried.

### Names

Name functions by address (`func_XXXXXXXX`), types `Type1`, `Type2` ... and
members by offset (`f20` for the member at `0x20`) until you understand what
something does. Then give it a descriptive name of your own. Do not copy
identifiers, file names or directory names from any other source (see
`LEGAL.md`).

## 5. Pull requests and commits

- Small, focused commits: one function or one tool change.
- Run the build, the audit and `gen_progress_report.py --check` before pushing.
- Commit messages: a short summary line, then an optional body. Add
  `Co-Authored-By:` for anyone (or any tool) who helped, and nothing else
  tool-specific: no session links.
- Keep generated and private files out: `asm/`, `baserom/`, `build/`, `venv/`,
  `toolchain/` and `private/` are ignored by git. Never commit retail data.
- CI (`.github/workflows/progress.yml`) validates `progress/report.json` and
  uploads it to [decomp.dev](https://decomp.dev/Lynder63/rac-deadlocked-decomp).
  It does not build the game: the compiler and the executable cannot be
  redistributed, so the report is generated on your machine and committed.

## 6. Where things are

| Path | Contents |
|---|---|
| `src/core`, `src/net`, `src/game` | decompiled game code, one file per address |
| `src/libgcc`, `src/libm` | GCC runtime and newlib math sources that match |
| `include/` | `common.h` (types) and assembly macros |
| `config/` | splat configuration, section table, function list, library tables |
| `tools/` | build, audit, diff and report tools |
| `nonmatching/` | drafts that do not match yet (not built) |
| `docs/RESEARCH.md` | how the executable is built and how it is rebuilt |
| `docs/OVERLAYS.md` | the 47 level overlays and how they are split and counted |
| `docs/CREDITS.md`, `THIRD_PARTY_NOTICES.md` | sources and licences |
