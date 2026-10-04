#!/usr/bin/env python3
"""
Check every compiled function against the retail image.

Reads build/obj/*.o (tools/build.sh) and compares each `func_XXXXXXXX` with
the retail bytes at that address (and each `func_L<level>_<address>` with the bytes
in that level's overlay, found in $OVERLAYS or private/overlays). Fields a linker would fill in (jump
targets, the immediates of lui and of address arithmetic and loads/stores)
are masked: this is NOT a link-time comparison, so a function that calls or
reads the wrong symbol can still count. Writes build/matches.json.

Usage: venv/bin/python tools/audit_matches.py
"""
import glob
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retail as mp  # noqa: E402
from elftools.elf.elffile import ELFFile  # noqa: E402

ROOT = mp.ROOT


def main() -> int:
    sizes = {}
    for l in (ROOT / "config" / "functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            n, a, s, _ = l.split("\t")
            sizes[n] = (int(a, 16), int(s, 16))
    with open(ROOT / "baserom" / "SCUS_974.65.elf", "rb") as f:
        secs = mp.sections(ELFFile(f))
    # level overlay functions (func_L<level>_<address>): retail bytes come from the
    # overlay ELFs of an unpacked disc (docs/OVERLAYS.md): $OVERLAYS or private/overlays
    ovl = {}
    for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            n, a, sz, _, _ = l.split("\t")
            ovl[n] = (n.split("_")[1], int(a, 16), int(sz, 16))
    ovl_dirs = {}
    for l in (ROOT / "config" / "overlays.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            i, d, _, _ = l.split("\t")
            ovl_dirs[i] = d
    ovl_root = Path(os.environ.get("OVERLAYS") or ROOT / "private" / "overlays")
    ovl_secs = {}

    def overlay_secs(i):
        if i not in ovl_secs:
            p = ovl_root / "levels" / ovl_dirs[i] / "overlay.elf"
            ovl_secs[i] = mp.sections(ELFFile(open(p, "rb"))) if p.exists() else None
        return ovl_secs[i]
    # libgcc objects (tools/build_libgcc.sh) are verbatim GCC source: their
    # symbols are paired with retail addresses by config/libgcc.tsv.
    alias = {}
    by_addr = {a: n for n, (a, _) in sizes.items()}
    for tsv in ("libgcc.tsv", "libm.tsv"):
        lg = ROOT / "config" / tsv
        if lg.exists():
            for l in lg.read_text().splitlines():
                if l and not l.startswith("#"):
                    obj, sym, a, _ = l.split("\t")
                    alias[(obj[:-2] if obj.endswith(".o") else obj, sym)] = by_addr[int(a, 16)]
    exact, bad = [], []
    for path in sorted(glob.glob(str(ROOT / "build" / "obj" / "*.o")) + glob.glob(str(ROOT / "build" / "libgcc" / "*.o")) + glob.glob(str(ROOT / "build" / "libm" / "*.o"))):
        elf = ELFFile(open(path, "rb"))
        text = elf.get_section_by_name(".text")
        data = text.data() if text else b""
        for s in elf.get_section_by_name(".symtab").iter_symbols():
            if s["st_info"]["type"] != "STT_FUNC":
                continue
            name = alias.get((Path(path).stem, s.name))
            if name is None:
                if not re.fullmatch(r"func_(L\d\d_)?[0-9A-F]{8}", s.name):
                    continue
                name = s.name
            if name in ovl:
                lvl, addr, size = ovl[name]
                osecs = overlay_secs(lvl)
                if osecs is None:
                    bad.append((s.name, "overlay data not found (set OVERLAYS)"))
                    continue
                code = data[s["st_value"]: s["st_value"] + s["st_size"]]
                retail = mp.read(osecs, addr, size)
            else:
                addr, size = sizes.get(name, (None, None))
                if addr is None:
                    bad.append((s.name, "not in config/functions.tsv"))
                    continue
                code = data[s["st_value"]: s["st_value"] + s["st_size"]]
                retail = mp.read(secs, addr, size)
            # The linker pads functions to 8 bytes with nops: those belong to
            # the retail function but not to the compiled one.
            pad = size - len(code)
            if 0 < pad <= 12 and not any(retail[len(code):]):
                retail = retail[:len(code)]
                size = len(code)
            if len(code) == size and mp.normalise(code) == mp.normalise(retail):
                exact.append(name)
            else:
                bad.append((s.name, "size %d vs retail %d" % (len(code), size)
                            if len(code) != size else "bytes differ"))
    (ROOT / "build").mkdir(exist_ok=True)
    (ROOT / "build" / "matches.json").write_text(json.dumps({"exact": sorted(exact)}, indent=1))
    print("%d exact, %d not exact" % (len(exact), len(bad)))
    for n, why in bad:
        print("  %s: %s" % (n, why))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
