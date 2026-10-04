#!/usr/bin/env bash
# Build the math library sources (newlib's libm/math, 2000-02-17 snapshot, kept
# under private/newlib or src/libm) the way Sony's libm.a was built: Sony's
# 2.9-ee driver. Output: build/libm/<member>.o for every member in config/libm.tsv.
#   bash tools/docker/run.sh bash tools/build_libm.sh [extra flags]
set -u
cd "$(dirname "$0")/.."
export WINEDEBUG=-all
CC=toolchain/sn-prodg-24/local/sce/ee/gcc/bin/ee-gcc.exe
SRC=${LIBM_SRC:-src/libm}
INC="-I$SRC -Iprivate/include -I${LIBM_INC:-private/newlib/newlib/libc/include}"
FLAGS=${LIBM_FLAGS:--O2 -G2}
rm -rf build/libm; mkdir -p build/libm
n=0
for m in $(grep -v '^#' config/libm.tsv | cut -f1 | sort -u); do
  stem=${m%.o}
  [ -f "$SRC/$stem.c" ] || continue
  wine $CC $FLAGS -c $INC "$SRC/$stem.c" -o build/libm/$stem.o >/dev/null 2>build/libm/$stem.err || true
  n=$((n+1))
done
echo "compiled $n files"
