# Research notes

How the retail executable is built and how it is rebuilt here. Everything below
was derived from the retail NTSC-U executable (`SCUS_974.65`, `VER = 1.00`,
SHA-1 `aa91b1c3b9b1a244320c47580b77342ef9856e95`), the compilers and libraries
that ship with the toolchain mirrors, and public documentation (wrench, the
Up Your Arsenal and R&C1 decompilations, GCC and its libgcc sources).

## The retail executable

`SCUS_974.65` is 1,692,216 bytes: a small loader plus one compressed game image.

| | |
|---|---|
| ELF | 32-bit LE, `EXEC`, entry `0x800008`, one `LOAD` segment, no symbol table |
| Loader | `.text`, 20 KB at `0x800000`: kernel startup, TLB setup, and an LZO1X-style decompressor at `0x800160` |
| Payload | a `WAD` blob at file offset `0x7080`, 1,662,911 bytes, in `.rodata` |

The disc's ISO9660 filesystem holds only the loader, the IOP image and the DNAS
and network GUI files; the rest of the image is read by sector number, outside
the filesystem (see wrench's `docs/file_loading.md`).

### The packed image

The payload starts with `WAD`, a `u32` compressed size and 9 bytes of padding,
then packets in an LZO1X-style format. The compressor pads at every 0x2000-byte
boundary with a `12 00 00` packet followed by `0xEE` fill, because the game
streams the data through the scratchpad in 0x2000 blocks. Decoding state and
the match window continue across those boundaries. `tools/unpack_wad.py`
decodes it: **5,157,636 bytes**, ending exactly at the declared size.

The unpacked image is a stream of 16-byte headers (`dest`, `size`, ELF type,
entry) each followed by its data: **17 sections**, entry point `0x1574E8`.
`tools/split_image.py` splits them and builds `baserom/SCUS_974.65.elf` (one
segment per section) for splat. `config/sections.txt` lists them:

| Section | Address | Size |
|---|---|---|
| `.vutext` | `0x00100080` | `0x1A0E0` |
| `core.text` | `0x0011A180` | `0x49990` |
| `core.data` | `0x00163B80` | `0x2E350` |
| `core.rdata` | `0x00191F00` | `0x13248` |
| `core.bss` | `0x001A5180` | `0x78AB8` |
| `core.lit`, `.lit` | `0x0021DC80`, `0x0021E180` | `0x4B8`, `0x2EF0` |
| `.bss` | `0x00221080` | `0x1A4908` |
| `.data` | `0x003C5A00` | `0x2B404` |
| `lvl.vtbl`, `lvl.camvtbl`, `lvl.sndvtbl` | `0x003F0E80`, `0x003F0F00`, `0x003F0F80` | `0xC`, `0x14`, `0x8` |
| `.text` (level code) | `0x003F1000` | `0x15C6D8` |
| `patch.data` | `0x0054D700` | `0x18` |
| `net.text` | `0x01E9A000` | `0x97330` |
| `net.nostomp` | `0x01F31380` | `0x6C20` |

Level code lives in `.text` and `.data`; those sections are overwritten when a
level loads, and each of the 47 levels carries its own overlay on the disc
(table of contents at sector 1001). The resident `.text` is the menus' code: 97
percent of it is inside the multiplayer menu overlay. See `docs/OVERLAYS.md`.

## Disassembly

`config/splat.yaml` (one segment per section) and `bash tools/setup_asm.sh`
generate `asm/`: **8,027 functions** (`core_text` 1,710, `net_text` 2,434, level
`.text` 3,883).

Level `.text` embeds scrambled data inside functions (a `b` jumps over it). The
words include fake branches, and splat then treats the first function as
running to the end of the section. `tools/find_functions.py` finds function
boundaries itself (section start, `jal` targets, after `jr $ra` plus delay
slot) into `config/symbol_addrs.txt` and gives each function with invalid
instructions its own subsegment (22 of them). A few still come out very large
and need their boundaries fixed by hand. `core.bss` and `.bss` are not split yet.

## The compiler

**SN GCC 2.95.3 v1.36** (`ee-gcc2953.exe` from the ProDG 3.01 mirror), flags

```
-O2 -G8 -fopt-stack -mno-check-zero-division
```

plus `-mno-split-addresses` for some files (a source file says so with
`/* cflags: -mno-split-addresses */` on its first line; `tools/build.sh` reads it).

How it was found. Five small functions whose C is certain from the assembly
were compiled with every compiler in the mirrors and compared with retail
(exact matches out of 5 / same size out of 5):

| Compiler | `-O2` | Notes |
|---|---|---|
| **SN GCC 2.95.3 v1.36** (`sn-prodg-3.01` `ee-gcc2953.exe`) | **4 / 5**, 5 / 5 | the remaining function differed in one register |
| Sony 2.9-ee-991111 (`ee-gcc.exe`) | 3 / 5, 4 / 5 | wrong code for one function |
| SN 1.14 (`sn-prodg-24` `ee-gcc2953.exe`) | 1 / 5, 5 / 5 | |
| SN 2.74 (`ee-gcc295.exe`) | 1 / 5, 5 / 5 | |

The Up Your Arsenal decomp reports the same compiler (its
`compiler_matrix_findings.md`), and also supplied the flags below.

- **`-fopt-stack`** (SN only): retail saves callee-saved registers with `sd`/`ld`
  in compact 8-byte slots (`s0` at 0, `s1` at 8, `ra` at 0x10). Without the flag
  the compiler emits `sq`/`lq` pairs in 16-byte slots, and every function that
  saves two or more registers fails.
- **`-G8`**: of retail's `$gp`-relative accesses, 1,799 are `lw`, 917 `sw`, 330
  `lwc1` and 18 are 8-byte `ld`/`sd`, so the small-data threshold is 8. Globals
  that retail reads with `lui`/`lw` are declared without a size
  (`extern T x[];` plus `#define x (x[0])`) so the compiler does not put them in
  `.sdata`.
- **`-mno-split-addresses`**: makes the compiler emit a global access as one
  assembler macro, and the assembler then uses the destination register as the
  temporary (`lui $a0; lw $a0, lo($a0)`). Without it the compiler splits the
  access itself and picks another register. Which files need it differs (the Up
  Your Arsenal decomp reports the same, in runs of consecutive functions).
- **`-mno-check-zero-division`**: no `break 7` after `div` (not yet needed here).

Source-level findings: a counter that retail reloads from memory needs
`volatile`; `p = array + i` gives a different register order than
`array[i].field`; an `s8` parameter compared with -1 adds sign extensions that
retail does not have (use `s32`).

### The assembler

Retail's code was assembled by SN's own assembler (`ps2eeas`), not by the GNU
`as` the compiler driver calls. It differs in ways that show up as extra nops
and different constant sequences. `tools/cc.sh` reproduces them in two extra
steps around the normal compile (compile to assembly, expand 64-bit constants as
`ps2eeas` does, assemble once, add the nops `ps2eeas` adds, assemble again), with
`tools/ps2eeas_dli.py` and `tools/ps2eeas_nops.py` taken from rac1-decomp,
which measured the real assembler. The rules: loops shorter than a minimum are
padded with nops (here, 5 instructions target through branch, 6 with the
branch's delay slot: the retail histogram of backward branches in level code
starts at 5), a float compare followed directly by `bc1` gets a nop between them,
and an `mtc1` whose destination is read by the next instruction gets one too.
Retail's level code has 722 `mtc1; nop; cvt.s.w` sequences and 93 without; the
nop pass accounts for the first group.

Not explained yet: retail has two nops before most `div.s` (281 of 435 in level code,
including library code), while the compilers in the mirrors emit none and `ps2eeas` on
small test cases adds none either; in the library code the compiler puts the `div.s` in
a jump's delay slot and retail does not.

Other near misses are a delay slot that retail leaves empty, or a register move
that retail schedules before a save where the compiler puts it after.

## libgcc

The GCC runtime library is linked in at `0x12EE30` to `0x131958`. Those functions
were not written for the game: they are GCC's own sources built by Sony's
toolchain, so they are rebuilt from GCC's sources (`src/libgcc/README.md`),
the same way as in rac1-decomp: Sony's 2.9-ee driver, `-O2 -G2`, one object per
module, soft-float as two whole-file objects. `tools/build_libgcc.sh` builds,
`tools/map_libgcc.py` pairs each compiled function with its retail address
(`config/libgcc.tsv`). 24 of the 36 functions match. `__moddi3` and
`__umoddi3` come out at the right size with 7 and 2 words different (retail's
stack frame is larger), `__udivdi3` is 12 bytes short. Sony's prebuilt
`libgcc.a` matches retail for all three, so retail linked that archive;
the archive is a reference only and not a substitute.

## libm

The math library (`__ieee754_*`, `sqrtf`, `floorf` ...) is newlib's libm
(fdlibm), built by Sony's 2.9-ee driver with `-O2 -G2`, the same as libgcc.
`tools/map_archive.py` pairs the functions of the library archive in the
toolchain mirror with retail (`config/libm.tsv`: 40 functions, 20,220 bytes);
`tools/build_libm.sh` builds newlib's sources (snapshot 2000-02-17,
`tools/get_newlib.sh`). 27 of the 40 members match exactly (7,744 bytes);
`src/libm/README.md` lists the rest.

## Checking matches

`tools/audit_matches.py` compares every compiled function with the retail bytes
at its address, with relocatable fields masked (`tools/retail.py`). This is not
a link-time comparison, so a function that calls or reads the wrong symbol can
still count. `tools/diff_func.py` shows a function next to retail word by word;
`tools/try_variants.py` tries several source forms of one function at once.
`tools/gen_progress_report.py` writes `progress/report.json` for decomp.dev
from `config/functions.tsv` and the audit result.

## Open questions

1. A linked image and a link-time comparison (relocations included).
2. The level overlays on the disc and their load addresses.
3. The float `nop` pattern above, and the scheduling differences.
4. `__moddi3`, `__udivdi3` and `__umoddi3` from source.
5. Splitting `core.bss` and `.bss`.
