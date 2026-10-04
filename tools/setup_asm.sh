#!/usr/bin/env bash
# Generate asm/ from your own baserom/SCUS_974.65 (never committed).
#   1. unpack the game image from the loader     (tools/unpack_wad.py)
#   2. split it into sections and rebuild an ELF (tools/split_image.py)
#   3. run splat on the ELF                      (config/splat.yaml)
set -euo pipefail
cd "$(dirname "$0")/.."

EXPECTED=aa91b1c3b9b1a244320c47580b77342ef9856e95
[ -f baserom/SCUS_974.65 ] || { echo "put your SCUS_974.65 in baserom/"; exit 1; }
ACTUAL=$(sha1sum baserom/SCUS_974.65 | cut -d' ' -f1)
[ "$ACTUAL" = "$EXPECTED" ] || { echo "baserom/SCUS_974.65 has sha1 $ACTUAL, expected $EXPECTED"; exit 1; }

if [ ! -x venv/bin/python ]; then
    python3 -m venv venv
    venv/bin/pip install -q -r requirements.txt
fi

venv/bin/python tools/unpack_wad.py
venv/bin/python tools/split_image.py
rm -rf asm
venv/bin/python -m splat split config/splat.yaml

# Optional: the level overlays. Set OVERLAYS to a folder made by
# `wrenchbuild unpack GAME.iso -o DIR -g dl -r us` (docs/OVERLAYS.md).
if [ -n "${OVERLAYS:-}" ]; then
    venv/bin/python tools/gen_overlay_asm.py "$OVERLAYS"
fi
