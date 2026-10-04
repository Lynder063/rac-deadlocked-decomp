#!/usr/bin/env python3
"""
Show a compiled function next to the retail one, word by word.
  venv/bin/python tools/diff_func.py func_00473A88
Reads build/obj/*.o (tools/build.sh) and the retail ELF. `=` marks words equal
after masking relocatable fields, `!` words that differ.
"""
import glob
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retail as mp  # noqa: E402
import rabbitizer  # noqa: E402
from elftools.elf.elffile import ELFFile  # noqa: E402

ROOT = mp.ROOT


def main() -> int:
    name = sys.argv[1]
    addr = size = None
    for l in (ROOT / "config" / "functions.tsv").read_text().splitlines():
        if l.startswith(name + "\t"):
            _, a, s, _ = l.split("\t")
            addr, size = int(a, 16), int(s, 16)
    elf_path = ROOT / "baserom" / "SCUS_974.65.elf"
    if addr is None:  # a level overlay function: func_L<level>_<address>
        import os
        for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
            if l.startswith(name + "\t"):
                _, a, s, _, _ = l.split("\t")
                addr, size = int(a, 16), int(s, 16)
        for l in (ROOT / "config" / "overlays.tsv").read_text().splitlines():
            if l.startswith(name.split("_")[1] + "\t"):
                d = l.split("\t")[1]
        elf_path = Path(os.environ.get("OVERLAYS") or ROOT / "private" / "overlays") / "levels" / d / "overlay.elf"
    with open(elf_path, "rb") as f:
        secs = mp.sections(ELFFile(f))
    retail = mp.read(secs, addr, size)
    code = b""
    for path in glob.glob(str(ROOT / "build" / "obj" / "*.o")):
        elf = ELFFile(open(path, "rb"))
        for s in elf.get_section_by_name(".symtab").iter_symbols():
            if s.name == name and s["st_info"]["type"] == "STT_FUNC":
                code = elf.get_section_by_name(".text").data()[s["st_value"]: s["st_value"] + s["st_size"]]
    dis = lambda w: rabbitizer.Instruction(w, 0, category=rabbitizer.InstrCategory.R5900).disassemble()
    n = max(len(code), len(retail)) // 4
    rn, cn = mp.normalise(retail), mp.normalise(code)
    for i in range(n):
        a = struct.unpack_from("<I", code, i * 4)[0] if i * 4 < len(code) else None
        b = struct.unpack_from("<I", retail, i * 4)[0] if i * 4 < len(retail) else None
        eq = i < len(cn) and i < len(rn) and cn[i] == rn[i]
        print("%s %-40s | %s" % ("=" if eq else "!", dis(a) if a is not None else "", dis(b) if b is not None else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
