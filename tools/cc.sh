#!/usr/bin/env bash
# Compile one C file the way retail was built:
#   1. SN GCC 2.95.3 v1.36 (-S)                              -> x.s
#   2. expand 64-bit constants like SN's assembler (dli)     -> x.s
#   3. assemble once with the driver's GNU as                -> x_first.o
#   4. add the nops SN's assembler (ps2eeas) adds            -> x_fixed.s
#   5. assemble again                                        -> OUT.o
# usage (inside the container): bash tools/cc.sh SRC.c OUT.o [extra compiler flags]
set -euo pipefail
cd "$(dirname "$0")/.."
src=$1; out=$2; shift 2
CC=toolchain/sn-prodg-3.01/usr/local/sce/ee/gcc/bin/ee-gcc2953.exe
export WINEDEBUG=-all
mkdir -p build/tmp
tmp=build/tmp/$(basename "${out%.o}")
wine "$CC" -O2 -G8 -fopt-stack -mno-check-zero-division "$@" -Iinclude -S "$src" -o "$tmp.s"
python tools/ps2eeas_dli.py "$tmp.s" "$tmp.s"
wine "$CC" -c "$tmp.s" -o "${tmp}_first.o"
python tools/ps2eeas_nops.py "$tmp.s" "${tmp}_first.o" "${tmp}_fixed.s"
wine "$CC" -c "${tmp}_fixed.s" -o "$out"
