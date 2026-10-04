# libm

Retail links the math library (`libm`) into `core_text`. These functions were
not written for the game: they are the sources of newlib's libm (fdlibm), built
by Sony's toolchain, so they are rebuilt from those sources unchanged.

- **Sources:** newlib, snapshot 2000-02-17 (`newlib/libm/math` and
  `newlib/libm/common`), copyright Sun Microsystems and others, under the
  permissive notices in each file's header (see `THIRD_PARTY_NOTICES.md`).
  Only the members that match retail are kept here (27 of 40 in the range);
  the rest are left out until they match.
- **Compiler:** Sony's `2.9-ee-991111` through its driver, `-O2 -G2`, one object
  per source file (`tools/build_libm.sh`; headers from the same snapshot via
  `tools/get_newlib.sh`). `-O3` and `-G0` give the same result, `-G8`, `-O1` and
  `-fno-strict-aliasing` are worse.
- **Mapping:** `config/libm.tsv` pairs each function with its retail address
  (`tools/map_archive.py`, from the library archive in the toolchain mirror);
  `tools/audit_matches.py` checks the bytes.
- **Not matching yet:** `e_fmod` (5 words differ), `e_sqrt` (same size, 20 words),
  `e_pow`, `s_rint`, and the float members `ef_asin`, `ef_exp`, `ef_log`,
  `ef_log10`, `ef_pow`, `ef_rem_pio2`, `ef_sqrt`, `wf_acos`: their size differs from
  retail by up to 0x7C bytes. Part of that is nops: retail has two nops before every
  `div.s` (also in the matching `__ieee754_sqrtf` body, where the compiler puts the
  `div.s` in a jump's delay slot and retail does not). None of the compilers in the
  mirrors, none of their machine flags, and none of the assemblers (the GNU `as`
  of either mirror, and `ps2eeas`, tested on small cases) produce those nops, so the
  rule behind them is still unknown. The rest points at a different revision of
  those files.
