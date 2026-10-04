#!/usr/bin/env python3
"""
Progress report for decomp.dev, in objdiff's report format (version 2).

decomp.dev reads a `report.json` that CI uploads as the artifact
`SCUS_974.65_report`. CI cannot build the game: the compiler and the retail
executable may not be redistributed. So the report is generated HERE, from a
real local build, and committed as progress/report.json. The workflow only
validates and uploads it. The report holds names, addresses, sizes and
percentages. It holds no retail bytes.

Inputs:
  config/functions.tsv   every function (tools/gen_function_list.py)
  src/**/*.c             decompiled functions, named func_XXXXXXXX
  build/matches.json     which of them match retail (tools/audit_matches.py)

A function counts as matched when its compiled code equals retail with
relocatable fields masked (see tools/audit_matches.py: not a link-time check).

Usage:
  python tools/gen_progress_report.py          write progress/report.json from
                                               the last build (tools/build.sh,
                                               tools/audit_matches.py)
  python tools/gen_progress_report.py --check  CI: the report must list as
                                               matched exactly the functions
                                               that have C source
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "progress" / "report.json"
FUNCTIONS = ROOT / "config" / "functions.tsv"
MATCHES = ROOT / "build" / "matches.json"

DEF_RE = re.compile(r"^[A-Za-z_][\w \t\*]*?\b(func_[0-9A-F]{8})\s*\(.*\)\s*\{?\s*$", re.M)

# Progress categories shown on decomp.dev.
CATEGORIES = [
    ("game", "Game"),
    ("core", "Core"),
    ("net", "Network"),
    ("level", "Level code"),
    ("libgcc", "libgcc"),
]
SEGMENT_CATEGORIES = {
    "core_text": ["core", "game"],
    "net_text": ["net", "game"],
    "text": ["level", "game"],
    "libgcc": ["libgcc", "game"],
}
# libgcc is GCC's own source built by Sony's compiler (src/libgcc/README.md);
# it occupies this part of core_text, and config/libgcc.tsv pairs the
# compiled symbols with retail addresses.
LIBGCC_RANGE = (0x12EE30, 0x131A00)
LIBGCC_TSV = ROOT / "config" / "libgcc.tsv"


def load_functions():
    funcs = {}
    for l in FUNCTIONS.read_text().splitlines():
        if l and not l.startswith("#"):
            name, addr, size, seg = l.split("\t")
            f = dict(name=name, addr=int(addr, 16), size=int(size, 16), seg=seg)
            if seg == "core_text" and LIBGCC_RANGE[0] <= f["addr"] < LIBGCC_RANGE[1]:
                f["seg"] = "libgcc"
            funcs[name] = f
    return funcs


def libgcc_functions():
    """(object, symbol, function name) rows of config/libgcc.tsv."""
    by_addr = {f["addr"]: n for n, f in load_functions().items()}
    rows = []
    if LIBGCC_TSV.exists():
        for l in LIBGCC_TSV.read_text().splitlines():
            if l and not l.startswith("#"):
                obj, sym, a, _ = l.split("\t")
                rows.append((obj, sym, by_addr[int(a, 16)]))
    return rows


def source_functions():
    """func_XXXXXXXX definitions in src/, by source file."""
    out = {}
    for p in sorted((ROOT / "src").rglob("*.c")):
        if p.parent.name == "libgcc":
            continue
        names = DEF_RE.findall(p.read_text(errors="ignore"))
        if names:
            out[p.relative_to(ROOT).as_posix()] = names
    # libgcc: one unit per compiled module, built from GCC's own source
    for obj, _, name in libgcc_functions():
        src = "src/libgcc/fp-bit.c" if obj.endswith("-bit") else "src/libgcc/libgcc2.c"
        out.setdefault(src + ":" + obj, []).append(name)
    return out


def measures(funcs, matched, units=None, complete_units=None):
    total = sum(f["size"] for f in funcs)
    got = sum(f["size"] for f in funcs if f["name"] in matched)
    m = {
        "fuzzy_match_percent": 100.0 * got / total if total else 0.0,
        "total_code": str(total),
        "matched_code": str(got),
        "matched_code_percent": 100.0 * got / total if total else 0.0,
        "total_functions": len(funcs),
        "matched_functions": sum(1 for f in funcs if f["name"] in matched),
        "complete_code": str(got if funcs and all(f["name"] in matched for f in funcs) else 0),
    }
    m["matched_functions_percent"] = 100.0 * m["matched_functions"] / len(funcs) if funcs else 0.0
    m["complete_code_percent"] = 100.0 * int(m["complete_code"]) / total if total else 0.0
    if units is not None:
        m["total_units"] = units
        m["complete_units"] = complete_units
    return m


def build_report(matched: set) -> dict:
    funcs = load_functions()
    by_src = source_functions()
    in_src = {}
    for path, names in by_src.items():
        for n in names:
            if n in funcs:
                in_src[n] = path
    units = []

    def add_unit(name, flist, source_path, cats):
        flist = sorted(flist, key=lambda f: f["addr"])
        off = 0
        fl = []
        for f in flist:
            fl.append({
                "name": f["name"], "size": str(f["size"]),
                "fuzzy_match_percent": 100.0 if f["name"] in matched else 0.0,
                "address": str(off),
                "metadata": {"virtual_address": str(f["addr"])},
            })
            off += f["size"]
        complete = bool(flist) and all(f["name"] in matched for f in flist)
        units.append({
            "name": name,
            "measures": measures(flist, matched, 1, 1 if complete else 0),
            "functions": fl,
            "metadata": {"complete": complete, "source_path": source_path,
                         "progress_categories": cats},
        })

    # one unit per source file
    for path, names in by_src.items():
        fl = [funcs[n] for n in names if n in funcs]
        if fl:
            src, _, obj = path.partition(":")
            uname = "libgcc/" + obj if obj else src[len("src/"):].rsplit(".", 1)[0]
            add_unit(uname, fl, src, SEGMENT_CATEGORIES[fl[0]["seg"]])
    # everything not decompiled yet, per segment
    rest = defaultdict(list)
    for n, f in funcs.items():
        if n not in in_src:
            rest[f["seg"]].append(f)
    for seg, fl in sorted(rest.items()):
        add_unit("asm/" + seg, fl, "asm/" + seg, SEGMENT_CATEGORIES[seg])

    all_funcs = list(funcs.values())
    complete_units = sum(1 for u in units if u["metadata"]["complete"])
    report = {
        "measures": measures(all_funcs, matched, len(units), complete_units),
        "units": units,
        "version": 2,
        "categories": [],
    }
    for cid, cname in CATEGORIES:
        cf = [f for f in all_funcs if cid in SEGMENT_CATEGORIES[f["seg"]]]
        report["categories"].append({"id": cid, "name": cname, "measures": measures(cf, matched)})
    return report


def check() -> int:
    try:
        r = json.loads(REPORT.read_text())
    except (OSError, ValueError) as e:
        print("progress/report.json unreadable: %s" % e)
        return 1
    if r.get("version") != 2 or "measures" not in r or "units" not in r:
        print("progress/report.json is not an objdiff v2 report")
        return 1
    reported = {f["name"] for u in r["units"] for f in u["functions"]
                if f["fuzzy_match_percent"] == 100.0}
    funcs = load_functions()
    in_src = {n for names in source_functions().values() for n in names if n in funcs}
    if reported != in_src:
        print("report out of date: matched in report but no C source: %s; "
              "C source but not matched in report: %s"
              % (sorted(reported - in_src)[:5], sorted(in_src - reported)[:5]))
        print("rebuild (tools/build.sh), audit (tools/audit_matches.py) and rerun "
              "tools/gen_progress_report.py")
        return 1
    print("progress/report.json OK (%d matched functions)" % len(reported))
    return 0


def main() -> int:
    if "--check" in sys.argv[1:]:
        return check()
    if not MATCHES.exists():
        print("run tools/build.sh and tools/audit_matches.py first")
        return 1
    matched = set(json.loads(MATCHES.read_text())["exact"])
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(build_report(matched), indent=1) + "\n")
    m = json.loads(REPORT.read_text())["measures"]
    print("wrote progress/report.json: %s/%s functions, %.3f%% code"
          % (m["matched_functions"], m["total_functions"], m["matched_code_percent"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
