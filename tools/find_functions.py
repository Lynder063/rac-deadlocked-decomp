#!/usr/bin/env python3
"""
Find function boundaries in the level `.text` section and write them to
config/symbol_addrs.txt.

Why: `.text` embeds data inside functions (a `b` jumps over it). The embedded
words include fake branches, which make splat's own search think the first
function never ends, so the whole section comes out as one huge function.

A function starts at the section start, at every `jal` target inside the
section, and right after a `jr $ra` plus its delay slot (skipping nops). It
ends where the next one starts. Names are address-based (`func_XXXXXXXX`).

It also rewrites the `text` segment of config/splat.yaml. splat stops
analysing a file at the first function that holds invalid instructions (the
embedded data), so every such function gets a subsegment of its own and the
clean runs between them are grouped.

Usage: venv/bin/python tools/find_functions.py     (needs baserom/sections/)
"""
import re
import struct
from pathlib import Path

import rabbitizer

ROOT = Path(__file__).resolve().parent.parent
SECTION = ROOT / "baserom" / "sections" / "13_text.bin"
VRAM = 0x3F1000
JR_RA = 0x03E00008
FILE_OFFSET = 0xD3A48   # file offset of the section in baserom/SCUS_974.65.elf
SPLAT = ROOT / "config" / "splat.yaml"


def main() -> int:
    d = SECTION.read_bytes()
    n = len(d) // 4
    w = struct.unpack("<%dI" % n, d[: n * 4])
    starts = {0}
    for i, x in enumerate(w):
        if x >> 26 == 3:  # jal
            tgt = ((x & 0x3FFFFFF) << 2) - VRAM
            if 0 <= tgt < n * 4:
                starts.add(tgt)
        if x == JR_RA and i + 2 < n:
            j = i + 2
            while j < n and w[j] == 0:
                j += 1
            if j < n:
                starts.add(j * 4)
    order = sorted(starts)
    lines = ["// Function boundaries of the level .text, from tools/find_functions.py"]
    for k, s in enumerate(order):
        end = order[k + 1] if k + 1 < len(order) else n * 4
        lines.append("func_%08X = 0x%X; // type:func size:0x%X" % (VRAM + s, VRAM + s, end - s))
    (ROOT / "config" / "symbol_addrs.txt").write_text("\n".join(lines) + "\n")
    print("%d functions in .text" % len(order))

    def dirty(a, b):
        for i in range(a // 4, b // 4):
            ins = rabbitizer.Instruction(w[i], VRAM + i * 4,
                                         category=rabbitizer.InstrCategory.R5900)
            if not ins.isValid():
                return True
        return False

    bounds = order + [n * 4]
    chunks = []  # (start, name)
    run_start = None
    for k, a in enumerate(order):
        if dirty(a, bounds[k + 1]):
            if run_start is not None:
                chunks.append((run_start, "text_%08X" % (VRAM + run_start)))
                run_start = None
            chunks.append((a, "text_%08X" % (VRAM + a)))
        elif run_start is None:
            run_start = a
    if run_start is not None:
        chunks.append((run_start, "text_%08X" % (VRAM + run_start)))
    body = "".join("      - [0x%X, c, %s]\n" % (FILE_OFFSET + a, nm) for a, nm in chunks)
    y = SPLAT.read_text()
    new = re.sub(r"(  - name: text\n    type: code\n    start: 0x[0-9A-F]+\n    vram: 0x[0-9A-F]+\n    subsegments:\n)(?:      - \[.*\]\n)+",
                 lambda m: m.group(1) + body, y, count=1)
    SPLAT.write_text(new)
    print("%d subsegments written to config/splat.yaml" % len(chunks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
