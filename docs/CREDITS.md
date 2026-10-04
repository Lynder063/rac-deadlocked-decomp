# Credits and sources

Everything below was consulted while building the project. Move this file with
the rest into the real repository.

## Community

- **GFI (Game Fuckery Inc.)** Discord: years of research and exploration of the
  games, which made this decompilation possible.

## Projects

| Project | Used for |
|---|---|
| [Lynder063/rac1-decomp](https://github.com/Lynder063/rac1-decomp) | Repository layout, README, progress workflow, report generator, toolchain notes, the libgcc build recipe, `tools/ps2eeas_nops.py` and `tools/ps2eeas_dli.py` (the nops and constant sequences of SN's assembler) |
| [OpenRAC](https://github.com/OpenRAC/OpenRAC) | Status of Deadlocked (`SCUS_974.65`), sourcing policy, game list |
| [vetusmagnus/ratchet-uya-decomp](https://github.com/vetusmagnus/ratchet-uya-decomp) | Up Your Arsenal compiler research (SN ee-gcc 2.95.3 v1.36), closest engine relative. Its `compiler_matrix_findings.md` supplied the `-fopt-stack`, `-G8` and global-declaration findings used here |
| [mateuszklysz/Lombyte](https://github.com/mateuszklysz/Lombyte) | R&C1 NTSC decomp, checked for Deadlocked coverage (none) |
| [chaoticgd/wrench](https://github.com/chaoticgd/wrench) | PS2 R&C asset toolkit; its docs (`docs/file_loading.md`, "WAD Compression") describe the packet format that `tools/unpack_wad.py` implements and the section layout of the executable |
| [AngheloAlf toolchain mirrors](https://github.com/AngheloAlf) | SN ProDG / PS2 SDK mirrors used by rac1-decomp |
| [decomp.dev](https://decomp.dev), [objdiff](https://github.com/encounter/objdiff), [splat](https://github.com/ethteck/splat), [spimdisasm](https://github.com/Decompollaborate/spimdisasm), [m2c](https://github.com/matt-kempster/m2c), [asm-differ](https://github.com/simonlindholm/asm-differ) | Tooling and progress tracking |
| [newlib](https://sourceware.org/newlib/) (fdlibm) | The math library sources in `src/libm/` (snapshot 2000-02-17, the same one rac1-decomp matched against), see `THIRD_PARTY_NOTICES.md` |
| [GCC](https://gcc.gnu.org) | `libgcc2.c`, `longlong.h`, `fp-bit.c` (GPL with the libgcc exception), see `THIRD_PARTY_NOTICES.md` |
