# libgcc

Retail links GCC's runtime library (`libgcc.a`) into `core_text` at
0x12EE30-0x131958. Those functions were not written for the game: they are
GCC's own sources built by Sony's EE toolchain, so they are rebuilt here from
GCC's sources rather than decompiled. Built the same way as in
[rac1-decomp](https://github.com/Lynder063/rac1-decomp), whose notes and
modified-in-place files these are taken from.

- Compiler: **Sony's `2.9-ee-991111`** (`ee-gcc.exe`) through its **driver**
  (`-O2 -G2 -S`, never `cc1` directly: the driver passes the target
  predefines that `longlong.h` selects its MIPS primitives from), then
  assembled by the SN driver. `tools/build_libgcc.sh`.
- One object per `L_*` module, plus two whole-file soft-float objects
  (`dp-bit.o`, and `fp-bit.o` with `-DFLOAT`) built with
  `-DFLOAT_BIT_ORDER_MISMATCH -DNO_DENORMALS -DUS_SOFTWARE_GOFAST`.
- `tools/map_libgcc.py` pairs each compiled function with its retail address
  (`config/libgcc.tsv`); `tools/audit_matches.py` checks the bytes. Retail's
  linker dead-stripped what the game never calls, so functions are compared
  one by one, not as whole objects.

Sony's prebuilt `libgcc.a` (in every `sn-prodg-24` and `sn-prodg-3.01` EE
compiler directory except 2.96-ee, which differs) matches retail for
`__moddi3`, `__udivdi3` and `__umoddi3` too, byte for byte (410, 372 and 336
of 410, 372 and 336 words). So retail linked that archive, and these three
objects came from a source revision or compile setup we have not reproduced
(`-g` changes nothing, nor does any compiler version selectable through the
`-V` option of the drivers present). The archive is a reference, never a
substitute: they stay unmatched until the C reproduces them.

Status: 24 of the 36 functions in the range match. `__moddi3`, `__udivdi3`
and `__umoddi3` do not yet: `__moddi3` and `__umoddi3` come out at the right
size with 7 and 2 words different (retail's stack frame is bigger), and
`__udivdi3` is 12 bytes shorter. rac1-decomp has the same residual. No
compiler flag tried (-O1..-O3, -G0, several `-f` options, four compilers)
changes it.

## Sources (GPL v2 with the libgcc linking exception, see each file's header)

| file | origin |
|---|---|
| `libgcc2.c`, `gbl-ctors.h`, `longlong.h` | GCC trunk at `31cf01446d` (1999-09-09) |
| `fp-bit.c` | GCC 2.95.3 release, with the two changes marked in place |
| `include/` | stand-ins for build-tree headers |
