#!/usr/bin/env python3
"""
Disassemble the level overlays with splat: asm/overlays/<id>/.

Every distinct overlay function is disassembled once, in the overlay where it
occurs first (the level id in its name, `func_<id>_<address>`). For each such
overlay this writes a splat configuration for its `overlay.elf`, with the
function boundaries and canonical names of config/overlay_functions.tsv (and
the resident functions of config/functions.tsv as external symbols, so calls
into the resident code are named), runs splat, and keeps only the functions that
belong to that overlay.

Needs the unpacked disc (see docs/OVERLAYS.md) and the venv.

Usage: venv/bin/python tools/gen_overlay_asm.py UNPACKED_DIR [LEVEL_ID ...]
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import split_overlays as so  # noqa: E402
import rabbitizer  # noqa: E402
from elftools.elf.elffile import ELFFile  # noqa: E402

ROOT = so.ROOT
OUT = ROOT / "asm" / "overlays"


def dirty(code, vram):
    """Does a function contain an invalid instruction (data embedded in it)?"""
    import struct
    for k, (w,) in enumerate(struct.iter_unpack("<I", code[: len(code) // 4 * 4])):
        if not rabbitizer.Instruction(w, vram + 4 * k, category=rabbitizer.InstrCategory.R5900).isValid():
            return True
    return False


def text_chunks(funcs, sh_addr, sh_offset):
    """splat subsegments for .text: every function with embedded data gets its own
    (splat gives up on the rest of a file at its first invalid instruction), the
    clean runs between them are grouped."""
    chunks, run = [], None
    for addr, size, code in funcs:
        if dirty(code, addr):
            if run is not None:
                chunks.append(run)
                run = None
            chunks.append(addr)
        elif run is None:
            run = addr
    if run is not None:
        chunks.append(run)
    return [("text_%08X" % a, sh_offset + (a - sh_addr)) for a in chunks]


def canonical_names(overlays):
    """digest -> canonical name, from config/overlay_functions.tsv."""
    by_key = {}
    for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            name, addr, size, cls, lv = l.split("\t")
            by_key[(name.split("_")[1], int(addr, 16))] = (name, cls)
    return by_key


def main() -> int:
    src = Path(sys.argv[1])
    only = set(sys.argv[2:])
    overlays = {}
    for l in (ROOT / "config" / "overlays.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            i, d, a, s = l.split("\t")
            overlays[i] = src / "levels" / d / "overlay.elf"
    # which overlay holds the first occurrence of each distinct function
    first = {}
    main_names = set()
    for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            name, addr, size, cls, lv = l.split("\t")
            if cls == "main":
                main_names.add(name)       # disassembled with the resident image
                continue
            first.setdefault(name.split("_")[1], []).append(name)
    # digest -> canonical name, over all overlays in id order
    digest_name = {}
    per_overlay = {}
    for i, path in overlays.items():
        t = ELFFile(open(path, "rb")).get_section_by_name(".text")
        fl = so.functions(t.data(), t["sh_addr"])
        per_overlay[i] = fl
    # canonical name of a digest = name of its first occurrence (tsv key: first id + address)
    tsv = {}
    for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            name, addr, size, cls, lv = l.split("\t")
            tsv[(name.split("_")[1], int(addr, 16))] = name
    for i, fl in per_overlay.items():
        for addr, size, code in fl:
            h = so.digest(code)
            nm = tsv.get((i, addr))
            if nm:
                digest_name.setdefault(h, nm)
    main_syms = []
    for l in (ROOT / "config" / "functions.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            n, a, s, seg = l.split("\t")
            main_syms.append((n, int(a, 16), int(s, 16)))
    OUT.mkdir(parents=True, exist_ok=True)
    for i in sorted(first):
        if only and i not in only:
            continue
        path = overlays[i]
        e = ELFFile(open(path, "rb"))
        work = OUT / i
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        # symbol file: canonical names for this overlay's functions + resident functions
        lines = []
        lo = e.get_section_by_name(".text")
        used = set()
        for addr, size, code in per_overlay[i]:
            nm = digest_name.get(so.digest(code))
            if nm and nm not in used:
                used.add(nm)
                lines.append("%s = 0x%X; // type:func size:0x%X" % (nm, addr, size))
            # a second copy inside one overlay keeps splat's own name (its file is dropped below)
        for n, a, s in main_syms:
            if 0x21E180 <= a < 0x1000000:      # the overlay's own range: not the resident code
                continue
            lines.append("%s = 0x%X; // type:func size:0x%X" % (n, a, s))
        (work / "symbol_addrs.txt").write_text("\n".join(lines) + "\n")
        # one splat segment per loadable section
        want = {".lit": "rodata", ".data": "data", "lvl.vtbl": "data", "lvl.camvtbl": "data",
                "lvl.sndvtbl": "data", ".text": "c"}
        secs = [s for s in e.iter_sections() if s.name in want]
        seg = []
        for s in secs:
            nm = s.name.lstrip(".").replace(".", "_")
            if s.name == ".text":
                subs = "\n".join("      - [0x%X, c, %s]" % (off, n)
                                 for n, off in text_chunks(per_overlay[i], s["sh_addr"], s["sh_offset"]))
            else:
                subs = "      - [0x%X, %s, %s]" % (s["sh_offset"], want[s.name], nm)
            seg.append("  - name: %s\n    type: code\n    start: 0x%X\n    vram: 0x%X\n    subsegments:\n%s"
                       % (nm, s["sh_offset"], s["sh_addr"], subs))
        end = max(s["sh_offset"] + s["sh_size"] for s in secs)
        yaml = """name: overlay_%s
options:
  basename: overlay_%s
  target_path: %s
  base_path: %s
  compiler: EEGCC
  platform: ps2
  asm_path: asm/overlays/%s
  src_path: src/overlays
  build_path: build/overlays/%s
  asset_path: asm/overlays/%s/assets
  disassemble_all: True
  matchings_path: nonmatchings
  create_c_files: False
  find_file_boundaries: True
  disasm_unknown: True
  generate_asm_macros_files: False
  symbol_addrs_path:
    - asm/overlays/%s/symbol_addrs.txt
segments:
%s
  - [0x%X]
""" % (i, i, path, ROOT, i, i, i, i, "\n".join(seg), end)
        (work / "splat.yaml").write_text(yaml)
        r = subprocess.run([str(ROOT / "venv" / "bin" / "python"), "-m", "splat", "split", str(work / "splat.yaml")],
                           capture_output=True, text=True, cwd=ROOT)
        # keep only the functions that belong to this overlay (the others are
        # disassembled where they occur first)
        removed = kept = 0
        for p in list((work / "nonmatchings").rglob("func_*.s")):
            m = re.match(r"func_(L\d\d)_[0-9A-F]{8}\.s$", p.name)
            if m and m.group(1) == i and p.stem not in main_names:
                kept += 1
            else:                           # earlier overlay's function, or a duplicate in this one
                p.unlink()
                removed += 1
        print("%s: %d functions kept, %d left out (earlier overlay or duplicate)%s" % (
            i, kept, removed, "" if r.returncode == 0 else "  (splat exit %d)" % r.returncode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
