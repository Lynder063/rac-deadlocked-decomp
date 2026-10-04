"""
Helpers for working with the retail image: reading its sections and comparing
code with relocatable fields masked.

normalise(): opcode and registers are kept, everything a linker or relocation
can change is masked (j/jal targets, the immediate of `lui`, and of loads,
stores and adds that are not stack-relative). Two functions that are equal
after this masking are the same code at different addresses.
"""
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J, JAL, LUI = 2, 3, 0x0F
MEM_OR_ADD = {0x08, 0x09, 0x0C, 0x0D, 0x0A, 0x0B, 0x20, 0x21, 0x23, 0x24, 0x25, 0x28,
              0x29, 0x2B, 0x31, 0x39, 0x37, 0x3F, 0x1E, 0x1F, 0x35, 0x3D, 0x27, 0x2F}


def normalise(code: bytes):
    out = []
    for (w,) in struct.iter_unpack("<I", code[: len(code) // 4 * 4]):
        op = w >> 26
        if op in (J, JAL):
            w = op << 26
        elif op == LUI:
            w &= 0xFFFF0000
        elif op in MEM_OR_ADD and ((w >> 21) & 31) != 29:
            w &= 0xFFFF0000
        out.append(w)
    return tuple(out)


def sections(elf):
    return [(s["sh_addr"], s["sh_size"], s.name, s.data() if s["sh_type"] != "SHT_NOBITS" else b"")
            for s in elf.iter_sections() if s["sh_addr"]]


def read(secs, addr, size):
    for a, n, _, d in secs:
        if a <= addr and addr + size <= a + n and d:
            return d[addr - a: addr - a + size]
    return None
