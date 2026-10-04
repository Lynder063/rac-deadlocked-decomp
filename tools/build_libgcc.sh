#!/usr/bin/env bash
# Build libgcc the way Sony's libgcc.a was built: GCC's own sources through
# Sony's 2.9-ee driver (-O2 -G2 -S), assembled by the SN driver. One object per
# L_* module, plus the two whole-file soft-float objects. Output: build/libgcc/.
#   bash tools/docker/run.sh bash tools/build_libgcc.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export WINEDEBUG=-all
BIN24=toolchain/sn-prodg-24/local/sce/ee/gcc/bin
CC_LIBGCC="wine $BIN24/ee-gcc.exe"
CC_TEXT="wine $BIN24/ee-gcc2953.exe"
FLAGS="-O2 -G2 -S"
FP_DEFS="-DFLOAT_BIT_ORDER_MISMATCH -DNO_DENORMALS -DUS_SOFTWARE_GOFAST"
out=build/libgcc; rm -rf "$out"; mkdir -p "$out"
for m in divdi3 moddi3 udivdi3 umoddi3 muldi3 fixdfdi fixunsdfdi floatdidf _main; do
    $CC_LIBGCC $FLAGS -Isrc/libgcc/include -DIN_LIBGCC2 -DL_$m src/libgcc/libgcc2.c -o $out/l2_$m.s
    $CC_TEXT -c $out/l2_$m.s -o $out/l2_$m.o
done
$CC_LIBGCC $FLAGS $FP_DEFS src/libgcc/fp-bit.c -o $out/dp-bit.s
$CC_TEXT -c $out/dp-bit.s -o $out/dp-bit.o
$CC_LIBGCC $FLAGS $FP_DEFS -DFLOAT src/libgcc/fp-bit.c -o $out/fp-bit.s
$CC_TEXT -c $out/fp-bit.s -o $out/fp-bit.o
ls $out/*.o | wc -l
