#!/usr/bin/env bash
# Compile every src/**/*.c with the matching compiler into build/obj/.
#   bash tools/docker/run.sh bash tools/build.sh      (Linux/macOS)
# Compiler: SN GCC 2.95.3 v1.36 from the ProDG 3.01 mirror, -O2 -G8 -fopt-stack
# (SN-only flag: 8-byte register save slots, as retail; found by the UYA decomp).
set -euo pipefail
cd "$(dirname "$0")/.."
CC=toolchain/sn-prodg-3.01/usr/local/sce/ee/gcc/bin/ee-gcc2953.exe
export WINEDEBUG=-all
rm -rf build/obj && mkdir -p build/obj
n=0
while IFS= read -r f; do
    o=build/obj/$(echo "${f#src/}" | tr '/' '_' | sed 's/\.c$/.o/')
    # a file may add flags with a first-lines comment:  /* cflags: -mno-split-addresses */
    extra=$(head -3 "$f" | sed -n 's#^/\* cflags: \(.*\) \*/#\1#p')
    bash tools/cc.sh "$f" "$o" $extra
    n=$((n+1))
done < <(find src -name '*.c' -not -path 'src/libgcc/*' -not -path 'src/libm/*' | sort)
echo "compiled $n files into build/obj/"
