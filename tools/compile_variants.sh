#!/usr/bin/env bash
# Compile one C file with every mirrored SN/Sony compiler and a few flag sets,
# writing build/variants/<compiler>_<flags>.s for comparison with retail.
#   bash tools/docker/run.sh bash tools/compile_variants.sh file.c
set -u
cd "$(dirname "$0")/.."
src=${1:?usage: compile_variants.sh file.c}
out=build/variants; mkdir -p "$out"
export WINEDEBUG=-all
declare -A CC=(
  [sn114]=toolchain/sn-prodg-24/local/sce/ee/gcc/bin/ee-gcc2953.exe
  [sn274]=toolchain/sn-prodg-24/local/sce/ee/gcc/bin/ee-gcc295.exe
  [sony29]=toolchain/sn-prodg-24/local/sce/ee/gcc/bin/ee-gcc.exe
  [sn136]=toolchain/sn-prodg-3.01/usr/local/sce/ee/gcc/bin/ee-gcc2953.exe
  [sn301]=toolchain/sn-prodg-3.01/usr/local/sce/ee/gcc/bin/ee-gcc.exe
)
for name in "${!CC[@]}"; do
  for flags in "-O2 -G0" "-O2 -G2" "-O2 -G8" "-O1 -G0" "-O3 -G0"; do
    tag=$(echo "$flags" | tr -d ' ')
    wine "${CC[$name]}" $flags -c "$src" -o "$out/${name}_${tag}.o" >/dev/null 2>"$out/${name}_${tag}.err" || echo "fail $name $flags"
  done
done
ls "$out"/*.o | wc -l
