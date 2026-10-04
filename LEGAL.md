# Legal scope of this project

This repository is a **matching decompilation** of *Ratchet: Deadlocked* (2005,
PS2; *Ratchet: Gladiator* in PAL regions), NTSC-U version. It produces C source
that, when compiled, reassembles to the original retail executable.

## This repo never contains

- The disc image, the retail executable, ELFs, or any file extracted from a disc.
- Asset binaries (textures, models, audio, level data).
- `asm/`: the disassembly carries retail instruction bytes, so each contributor
  generates it locally from their own baserom (`bash tools/setup_asm.sh`). It
  is gitignored.
- Compiler or SDK binaries, or patches that bypass copy protection.

## This repo does contain

- Source that a contributor wrote from the locally generated disassembly.
- Build scripts and config that describe how to rebuild the original layout
  from a baserom the user supplies.
- Names, addresses, sizes and percentages (`progress/report.json`).

## Contributors must supply themselves

- Their own legally obtained copy of the game, dumped by them.
- The compiler toolchain, obtained on their own.

## Sources

Allowed: the retail binary, SDK library *binaries* the toolchain ships, open
source code under its own license (credited in `THIRD_PARTY_NOTICES.md`), and
other public decompilations (credited).

**Never** use Sony's SDK source, samples or headers, or any leaked or NDA
material, not even as a reference to check a match against.

## Naming

Every name in this repository comes from the contributors' own work on the
retail binary: `func_XXXXXXXX` by address, generated type and member names
(`Type1`, `f20` for the member at offset 0x20), or a descriptive name given
after the function was understood from the retail code. Do not copy identifiers,
file names or directory names from any other source, and do not rename one
mechanically into a similar one. Reference material of any kind that is not
the retail binary lives under `private/` or `baserom/`, both ignored by git, and
nothing from it is written anywhere else.

Before every push: `git grep` for any name you are unsure about, and check the
history with `git log -S<name>`.
