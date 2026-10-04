#!/usr/bin/env python3
"""
Unpack the game image packed inside the retail loader executable.

The retail SCUS_974.65 is a small loader (.text at 0x800000) plus one
"WAD"-compressed blob in .rodata. The loader's own decompressor
(0x800160) is an LZO1X-style LZ decoder; this script does the same in
Python. The result is the flat game image: a stream of sections (.vutext,
core.text, .text, ...) as listed in the wrench documentation.

Format, as documented by the wrench project (docs/file_loading.md, "WAD
Compression") and confirmed against the loader's code:

  0x00  "WAD"
  0x03  u32 compressed size, including this header
  0x07  9 bytes padding
  0x10  stream of LZO1X-style packets

A packet `11/12 00 00` (distance 0, optional squashed literal in the low two
bits of the second byte) is a no-op. The compressor uses it at 0x2000-byte
boundaries, followed by 0xEE fill until (pos - wad_start) % 0x2000 == 0x10,
because the game streams the data through the scratchpad in 0x2000 blocks.
Decoding state and the match window continue across those boundaries.

Usage:
  python tools/unpack_wad.py [SCUS_974.65] [out.bin]

Defaults: baserom/SCUS_974.65 -> baserom/SCUS_974.65.unpacked
No retail bytes are part of this repository; the output stays in baserom/.
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAD_MAGIC = b"WAD"
BLOCK = 0x2000
HEADER = 0x10


def find_wad(data: bytes) -> int:
    """Offset of the compressed blob: the 'WAD' header inside .rodata."""
    pos = data.find(WAD_MAGIC, 0x1000)
    while pos >= 0:
        total = struct.unpack_from("<I", data, pos + 3)[0]
        if pos + total <= len(data) and data[pos + 7:pos + HEADER] == bytes(9):
            return pos
        pos = data.find(WAD_MAGIC, pos + 1)
    raise ValueError("no WAD header found")


def decompress(src: bytes, base: int) -> bytes:
    end = base + struct.unpack_from("<I", src, base + 3)[0]
    ip = base + HEADER
    out = bytearray()

    def copy_match(dist: int, length: int):
        s = len(out) - dist
        if s < 0:
            raise ValueError("bad match distance at input 0x%x" % ip)
        for _ in range(length):
            out.append(out[s])
            s += 1

    state = 0
    if src[ip] > 17:
        t = src[ip] - 17
        ip += 1
        out += src[ip:ip + t]
        ip += t
        state = 4 if t >= 4 else t

    while ip < end:
        t = src[ip]
        ip += 1
        if t < 16:
            if state == 0:
                if t == 0:
                    while src[ip] == 0:
                        t += 255
                        ip += 1
                    t += 15 + src[ip]
                    ip += 1
                out += src[ip:ip + t + 3]
                ip += t + 3
                state = 4
                continue
            if state == 4:
                dist = 1 + 0x0800 + (t >> 2) + (src[ip] << 2)
                ip += 1
                copy_match(dist, 3)
            else:
                dist = 1 + (t >> 2) + (src[ip] << 2)
                ip += 1
                copy_match(dist, 2)
        elif t >= 64:
            dist = 1 + ((t >> 2) & 7) + (src[ip] << 3)
            ip += 1
            copy_match(dist, (t >> 5) - 1 + 2)
        elif t >= 32:
            t &= 31
            if t == 0:
                while src[ip] == 0:
                    t += 255
                    ip += 1
                t += 31 + src[ip]
                ip += 1
            dist = 1 + ((src[ip] | (src[ip + 1] << 8)) >> 2)
            ip += 2
            copy_match(dist, t + 2)
        else:
            far = (t & 8) << 11
            t &= 7
            if t == 0:
                while src[ip] == 0:
                    t += 255
                    ip += 1
                t += 7 + src[ip]
                ip += 1
            d = far + ((src[ip] | (src[ip + 1] << 8)) >> 2)
            ip += 2
            if d == 0:
                # padding packet; a squashed literal may follow
                state = src[ip - 2] & 3
                if state:
                    out += src[ip:ip + state]
                    ip += state
                else:
                    while (ip < end and (ip - base) % BLOCK != HEADER
                           and src[ip] == 0xEE):
                        ip += 1
                continue
            copy_match(d + 0x4000, t + 2)
        state = src[ip - 2] & 3
        if state:
            out += src[ip:ip + state]
            ip += state

    if ip != end:
        raise ValueError("stream overran its end: 0x%x != 0x%x" % (ip, end))
    return bytes(out)


def main() -> int:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "baserom" / "SCUS_974.65"
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.name + ".unpacked")
    data = src.read_bytes()
    base = find_wad(data)
    out = decompress(data, base)
    dst.write_bytes(out)
    print("WAD at file offset 0x%x, %d -> %d bytes (0x%x)"
          % (base, struct.unpack_from("<I", data, base + 3)[0], len(out), len(out)))
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
