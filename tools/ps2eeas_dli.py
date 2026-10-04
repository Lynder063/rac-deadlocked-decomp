#!/usr/bin/env python3
"""
Expand 64-bit constants (`dli`) the way retail's assembler did, in
compiled game code.

Retail's text was assembled by SN's ps2eeas, and ps2eeas builds a 64-bit
constant with its own sequence; GNU as picks a different one for many
values. For 0x8000000044 (a GS register value), ps2eeas writes
`ori 0x8000; dsll 24; ori 0x44` and GNU as `addiu 0x80; dsll32 0;
ori 0x44`. Both are three words, so only the bytes differ. For some
values the lengths differ too.

The algorithm below was reconstructed from ps2eeas's own output and
checked against it on 871 constants (random, sparse, negative, masks and
GS-register shapes), every one exact:

- values that fit 16 or 32 bits: addiu / ori / lui [+ ori], as GNU;
- -1 << k: `addiu -1` then a left shift; a low mask 2^k - 1: `addiu -1`
  then a logical right shift;
- anything else: the significant bits in 16-bit chunks, each left-aligned
  to the highest set bit still unplaced: `ori` for the first chunk (or
  `lui` when the top 16 bits are all ones, so that it sign-extends), then
  for each further chunk a left shift up to its position and an `ori`,
  and a final shift for trailing zero bits.

This rewrites each `dli` line into explicit instructions before the first
assembly, so tools/ps2eeas_nops.py measures the real code.

usage: python tools/ps2eeas_dli.py IN.s OUT.s
"""
import re
import sys

M64 = (1 << 64) - 1
DLI = re.compile(r"^(\s*)dli\s+(\$\w+)\s*,\s*(-?(?:0x[0-9A-Fa-f]+|\d+))\s*(#.*)?$")


def _shift(r, n, out, op="dsll"):
    while n > 0:
        if n >= 32:
            k = min(n, 63) - 32
            out.append(f"{op}32\t{r},{r},{k}")
            n -= 32 + k
        else:
            out.append(f"{op}\t{r},{r},{n}")
            n = 0


def expand(c: int, r: str) -> list[str]:
    """ps2eeas's instructions for `dli R, C`."""
    c &= M64
    v = c - (1 << 64) if c >> 63 else c
    if -0x8000 <= v < 0x8000:
        return [f"addiu\t{r},$0,{v}"]
    if 0 <= v < 0x10000:
        return [f"ori\t{r},$0,{v:#x}"]
    if -0x80000000 <= v < 0x80000000:
        out = [f"lui\t{r},{(v >> 16) & 0xFFFF:#x}"]
        if v & 0xFFFF:
            out.append(f"ori\t{r},{r},{v & 0xFFFF:#x}")
        return out
    low = (c & -c).bit_length() - 1
    if v < 0 and c >> low == M64 >> low:          # -1 << low
        out = [f"addiu\t{r},$0,-1"]
        _shift(r, low, out)
        return out
    if c == (1 << c.bit_length()) - 1:             # low mask
        out = [f"addiu\t{r},$0,-1"]
        _shift(r, 64 - c.bit_length(), out, "dsrl")
        return out
    if v >= 0 or c >> 48 != 0xFFFF:
        top, signed = c.bit_length() - 1, False    # highest set bit
    else:
        top = 63                                   # lowest bit of the leading ones
        while (c >> (top - 1)) & 1:
            top -= 1
        signed = True
    pos = max(top - 15, 0)
    chunk = (c >> pos) & 0xFFFF
    out = [f"lui\t{r},{chunk:#x}" if signed else f"ori\t{r},$0,{chunk:#x}"]
    pending = -16 if signed else 0                 # lui has shifted by 16 already
    while True:
        rest = c & ((1 << pos) - 1)
        if rest == 0:
            _shift(r, pos + pending, out)
            return out
        new = max(rest.bit_length() - 1 - 15, 0)
        _shift(r, pos - new + pending, out)
        pending = 0
        out.append(f"ori\t{r},{r},{(c >> new) & ((1 << (pos - new)) - 1) & 0xFFFF:#x}")
        pos = new


def main() -> None:
    src, dst = sys.argv[1:3]
    out, n = [], 0
    for line in open(src):
        m = DLI.match(line.rstrip("\n"))
        if m:
            indent, reg, value = m.group(1), m.group(2), int(m.group(3), 0)
            out += [f"{indent}{ins}\n" for ins in expand(value, reg)]
            n += 1
        else:
            out.append(line)
    open(dst, "w").writelines(out)
    print(f"ps2eeas_dli: {n} dli expanded {src} -> {dst}")


if __name__ == "__main__":
    main()
