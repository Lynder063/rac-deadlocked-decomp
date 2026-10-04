#!/usr/bin/env python3
"""
Compare compiler variants against retail functions.

  venv/bin/python tools/compare_variants.py SPEC.tsv
SPEC.tsv: lines `name<TAB>retail_addr_hex` (function names in the compiled .o
must equal `name`). Reads build/variants/*.o (tools/compile_variants.sh) and
the retail ELF. Prints, per variant, how many functions match exactly after
masking relocatable fields, and the total bytes that differ in size.
"""
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retail as mp  # noqa: E402
from elftools.elf.elffile import ELFFile  # noqa: E402

ROOT = mp.ROOT


def main() -> int:
    spec = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
    with open(ROOT / "baserom" / "SCUS_974.65.elf", "rb") as f:
        secs = mp.sections(ELFFile(f))
    retail = {}
    for name, addr in spec:
        a = int(addr, 16)
        retail[name] = a
    sizes = {}
    for l in open(ROOT / "config" / "functions.tsv").read().splitlines()[1:]:
        r = l.split("\t")
        sizes[int(r[1], 16)] = int(r[2], 16)
    results = []
    for path in sorted(glob.glob(str(ROOT / "build" / "variants" / "*.o"))):
        elf = ELFFile(open(path, "rb"))
        text = elf.get_section_by_name(".text")
        data = text.data()
        syms = {s.name: s for s in elf.get_section_by_name(".symtab").iter_symbols()
                if s["st_info"]["type"] == "STT_FUNC"}
        same = size_same = 0
        detail = []
        for name, a in retail.items():
            s = syms.get(name)
            if s is None:
                detail.append(name + ":missing")
                continue
            size = s["st_size"] or 0
            code = data[s["st_value"]: s["st_value"] + size]
            rc = mp.read(secs, a, sizes.get(a, size))
            if rc is None:
                continue
            if len(code) == len(rc):
                size_same += 1
            if mp.normalise(code) == mp.normalise(rc):
                same += 1
            else:
                eq = sum(1 for x, y in zip(mp.normalise(code), mp.normalise(rc)) if x == y)
                detail.append("%s:%d/%d w" % (name, eq, len(rc) // 4))
        results.append((same, size_same, Path(path).stem, detail))
    for same, size_same, tag, detail in sorted(results, reverse=True):
        print("%-24s exact %d/%d  same size %d/%d  %s" % (tag, same, len(retail), size_same, len(retail), " ".join(detail)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
