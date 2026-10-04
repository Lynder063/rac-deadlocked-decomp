# Third-party notices

## GCC runtime library (`src/libgcc/`)

`libgcc2.c`, `gbl-ctors.h`, `longlong.h` (GCC trunk, 1999-09-09) and
`fp-bit.c` (GCC 2.95.3): Copyright Free Software Foundation, Inc. Licensed
under the GNU General Public License version 2 or later with the libgcc
linking exception, as stated in each file's header. They are built unchanged
(except two edits marked in place in `fp-bit.c`) to reproduce the library
that Sony's toolchain linked into the game.

The selection and build recipe come from
[rac1-decomp](https://github.com/Lynder063/rac1-decomp) (MIT).
