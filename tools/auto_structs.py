#!/usr/bin/env python3
"""
Automatic decompilation of small functions with structures built from the
assembly alone.

m2c prints member accesses on pointers of unknown type as `arg0->unk20`. This
tool turns them into real C: for every variable accessed that way it declares a
structure whose members sit at the offsets used (named by offset, `f20`), takes
each member's type from how m2c uses it (the declared type of the variable it
is loaded into or stored from, a cast, a call through it, a further `->`), and
rewrites the accesses. The result is compiled with the retail pipeline
(tools/cc.sh) in four variants and compared with retail. No outside material
is used: everything comes from the retail bytes and m2c's output.

  venv/bin/python tools/auto_structs.py prepare [CLASS] [N]
        CLASS: overlay (default; common and level functions of the level
        overlays), or main (resident functions). Candidates are the smallest
        functions not in src/ yet.
  bash tools/docker/run.sh bash build/auto3/compile.sh
  venv/bin/python tools/auto_structs.py check
  venv/bin/python tools/auto_structs.py adopt
"""
import glob
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import retail as mp  # noqa: E402
from elftools.elf.elffile import ELFFile  # noqa: E402

ROOT = mp.ROOT
AUTO = ROOT / "build" / "auto3"
OVL_ROOT = Path(os.environ.get("OVERLAYS") or ROOT / "private" / "overlays")
VARIANTS = [("arr_split", True, ""), ("arr_nosplit", True, "-mno-split-addresses"),
            ("plain_split", False, ""), ("plain_nosplit", False, "-mno-split-addresses")]
SCALARS = {"s8": 1, "u8": 1, "s16": 2, "u16": 2, "s32": 4, "u32": 4, "f32": 4, "s64": 8, "u64": 8, "f64": 8}
MIN_SIZE, MAX_SIZE = 0x20, 0x180


# ---------------------------------------------------------------- m2c output
def declared_types(text):
    """name -> type for the parameters and locals m2c declares."""
    types = {}
    head = re.search(r"^[\w \*]+?\b(\w+)\s*\(([^)]*)\)\s*\{", text, re.M)
    if head:
        for p in head.group(2).split(","):
            p = p.strip()
            m = re.match(r"^(.*?)(\w+)$", p)
            if m and p != "void":
                types[m.group(2)] = m.group(1).strip()
    for m in re.finditer(r"^\s+((?:[su](?:8|16|32|64)|f32|f64|void \*|s32 \*|u8 \*|u16 \*|u32 \*|f32 \*)) ?(\w+);", text, re.M):
        types[m.group(2)] = m.group(1).strip()
    return types


ACCESS = re.compile(r"\b([A-Za-z_]\w*)((?:->unk[0-9A-F]+)+)")


def build_structs(text):
    """Return (new text, struct definitions) or None when the accesses cannot be typed."""
    types = declared_types(text)
    # member table: base variable -> {offset: Counter(type)}, nested chains as sub-structs
    members = defaultdict(lambda: defaultdict(Counter))
    nested = {}   # (struct key, offset) -> child struct key

    def key(base, path):
        return "S_" + base + "".join("_" + o for o in path)

    for line in text.splitlines():
        for m in ACCESS.finditer(line):
            base = m.group(1)
            offs = re.findall(r"->unk([0-9A-F]+)", m.group(2))
            if base not in types or "*" not in types[base]:
                return None
            path = []
            for k, o in enumerate(offs):
                cur = key(base, path)
                last = k == len(offs) - 1
                if not last:
                    nested[(cur, int(o, 16))] = key(base, path + [o])
                    members[cur][int(o, 16)]["ptr"] += 1
                else:
                    t = infer(line, m, types)
                    members[cur][int(o, 16)][t] += 1
                path.append(o)
    # one type per offset, no overlaps
    defs, order = {}, []
    for k, offs in members.items():
        fields, end = [], 0
        for o in sorted(offs):
            t = offs[o].most_common(1)[0][0]
            if t != "ptr" and (k, o) not in nested and len(offs[o]) > 1 and "s32" not in offs[o]:
                return None
            if (k, o) in nested:
                t = "ptr"
            size = 4 if t in ("ptr", "fn") else SCALARS[t]
            if o < end or o % size:
                return None
            fields.append((o, t))
            end = o + size
        defs[k] = fields
        order.append(k)
    out = []
    for k in sorted(defs, key=lambda x: (-x.count("_"), x)):   # children first
        body, cur = [], 0
        for o, t in defs[k]:
            if o > cur:
                body.append("    char _p%X[0x%X];" % (cur, o - cur))
            if t == "ptr":
                child = nested[(k, o)]
                body.append("    %s *f%X;" % (child, o))
                size = 4
            elif t == "fn":
                body.append("    s32 (*f%X)();" % o)
                size = 4
            else:
                body.append("    %s f%X;" % (t, o))
                size = SCALARS[t]
            cur = o + size
        out.append("typedef struct %s {\n%s\n} %s;" % (k, "\n".join(body), k))
    fwd = "".join("typedef struct %s %s;\n" % (k, k) for k in defs)
    # rewrite
    new = ACCESS.sub(lambda m: m.group(1) + re.sub(r"->unk", "->f", m.group(2)), text)
    for base in {k.split("_")[1] for k in defs}:
        new = re.sub(r"\bvoid \*(\s*)%s\b" % re.escape(base), r"S_%s *\1%s" % (base, base), new)
    return new, fwd + "\n".join(out) + "\n"


def infer(line, m, types):
    """Type of the member accessed at `m` in `line`."""
    expr = m.group(0)
    after = line[m.end():]
    if after.lstrip().startswith("(") and not re.search(r"==|!=|<|>", after[:2]):
        return "fn"
    # x = V->unk;  -> type of x
    mm = re.match(r"^\s*(\w+)\s*=\s*(?:\([^)]*\)\s*)?" + re.escape(expr) + r"\s*;", line)
    if mm and mm.group(1) in types:
        t = types[mm.group(1)]
        if t in SCALARS:
            return t
    # V->unk = (T) ...;  or  = x;
    mm = re.match(r"^\s*" + re.escape(expr) + r"\s*=\s*\((\w+)\)", line)
    if mm and mm.group(1) in SCALARS:
        return mm.group(1)
    mm = re.match(r"^\s*" + re.escape(expr) + r"\s*=\s*(\w+)\s*;", line)
    if mm and mm.group(1) in types and types[mm.group(1)] in SCALARS:
        return types[mm.group(1)]
    mm = re.match(r"^\s*" + re.escape(expr) + r"\s*=\s*(\d+\.?\d*f)\s*;", line)
    if mm:
        return "f32"
    # compared / used with a cast: (u8) V->unk
    mm = re.search(r"\((\w+)\)\s*" + re.escape(expr), line)
    if mm and mm.group(1) in SCALARS:
        return mm.group(1)
    return "s32"


def fix(text):
    """m2c output -> compilable body, or None."""
    if not text.strip() or any(k in text for k in ("M2C_", "saved_reg_gp", "bitwise")):
        return None
    if re.search(r"\bsp\b", text) or re.search(r"\b[A-Za-z_]\w*\.unk[0-9A-F]+", text):
        return None
    text = re.sub(r"\s*/\* (irregular|extern) \*/", lambda m: " /* extern */" if m.group(1) == "extern" else "", text)
    return text


def build_source(text, name, arrays):
    decls, body = [], []
    for line in text.splitlines():
        if re.match(r"^(extern .*;|\S.*\);\s*/\* extern \*/)", line) or line.endswith("/* extern */"):
            decls.append(line.replace("/* extern */", "").strip())
        else:
            body.append(line)
    res = build_structs("\n".join(body))
    if res is None:
        return None
    btxt, structs = res
    btxt = re.sub(r"\?\s*\*", "void *", btxt)
    btxt = re.sub(r"(^|[(,]\s*)\?(?=\s+[A-Za-z_])", r"\1s32", btxt, flags=re.M)
    out = ['#include "common.h"', "", structs]
    macros = []
    for d in decls:
        d = re.sub(r"\?\s*\*", "void *", d)
        d = re.sub(r"\?", "s32", d)
        m = re.match(r"^extern (.+?) (D_[0-9A-Fa-f]+);$", d)
        if m and arrays:
            out.append("extern %s %s_[];" % (m.group(1), m.group(2)))
            macros.append("#define %s (%s_[0])" % (m.group(2), m.group(2)))
        else:
            out.append(d)
    out += macros + ["", btxt]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- driver
def load(cls):
    dirs = {}
    for l in (ROOT / "config" / "overlays.tsv").read_text().splitlines():
        if l and not l.startswith("#"):
            i, d, _, _ = l.split("\t")
            dirs[i] = d
    rows = []
    if cls == "overlay":
        for l in (ROOT / "config" / "overlay_functions.tsv").read_text().splitlines():
            if l and not l.startswith("#"):
                n, a, s, c, lv = l.split("\t")
                if c != "main":
                    rows.append((n, int(a, 16), int(s, 16), n.split("_")[1], len(lv.split(","))))
    else:
        for l in (ROOT / "config" / "functions.tsv").read_text().splitlines():
            if l and not l.startswith("#"):
                n, a, s, seg = l.split("\t")
                rows.append((n, int(a, 16), int(s, 16), None, 1))
    return dirs, rows


def already_done():
    done = set()
    for p in (ROOT / "src").rglob("*.c"):
        done.update(re.findall(r"\b(func_(?:L\d\d_)?[0-9A-F]{8})\s*\(", p.read_text(errors="ignore")))
    return done


def retail_reader(dirs):
    main = mp.sections(ELFFile(open(ROOT / "baserom" / "SCUS_974.65.elf", "rb")))
    cache = {}

    def read(lvl, addr, size):
        if lvl is None:
            return mp.read(main, addr, size)
        if lvl not in cache:
            cache[lvl] = mp.sections(ELFFile(open(OVL_ROOT / "levels" / dirs[lvl] / "overlay.elf", "rb")))
        return mp.read(cache[lvl], addr, size)
    return read


def prepare(cls, limit):
    dirs, rows = load(cls)
    done = already_done()
    asm = {}
    base = ROOT / "asm" / ("overlays" if cls == "overlay" else "nonmatchings")
    for p in base.rglob("func_*.s"):
        asm[p.stem] = p
    # smallest first; among overlay functions the ones shared by most levels first
    cands = sorted((s, -k, n, a, lvl) for n, a, s, lvl, k in rows
                   if n not in done and n in asm and MIN_SIZE <= s <= MAX_SIZE)
    cands.sort(key=lambda c: (c[1], c[0]))
    AUTO.mkdir(parents=True, exist_ok=True)
    for old in glob.glob(str(AUTO / "*.c")) + glob.glob(str(AUTO / "obj" / "*.o")):
        Path(old).unlink()
    script = ["export WINEDEBUG=-all", "cd \"$(dirname \"$0\")/../..\"", "mkdir -p build/auto3/obj"]
    count = skipped = 0
    for s, k, n, a, lvl in cands:
        if count >= limit:
            break
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "ext" / "m2c" / "m2c.py"), "-t", "mipsee-gcc-c", str(asm[n])],
                           capture_output=True, text=True)
        out = fix(r.stdout)
        wrote = False
        if out:
            for vname, arrays, extra in VARIANTS:
                src = build_source(out, n, arrays)
                if src is None:
                    break
                (AUTO / ("%s.%s.c" % (n, vname))).write_text(src)
                script.append("bash tools/cc.sh build/auto3/%s.%s.c build/auto3/obj/%s.%s.o %s >/dev/null 2>&1"
                              % (n, vname, n, vname, extra))
                wrote = True
        if wrote:
            count += 1
        else:
            skipped += 1
    (AUTO / "compile.sh").write_text("\n".join(script) + "\n")
    print("prepared %d functions (%d skipped), %d compiles" % (count, skipped, count * len(VARIANTS)))


def check(cls):
    dirs, rows = load(cls)
    info = {n: (a, s, lvl) for n, a, s, lvl, _ in rows}
    read = retail_reader(dirs)
    exact, tried = {}, set()
    for path in sorted(glob.glob(str(AUTO / "obj" / "*.o"))):
        base = Path(path).name[:-2]
        name, _, variant = base.partition(".")
        tried.add(name)
        elf = ELFFile(open(path, "rb"))
        text = elf.get_section_by_name(".text")
        if text is None:
            continue
        data = text.data()
        for s in elf.get_section_by_name(".symtab").iter_symbols():
            if s.name != name or s["st_info"]["type"] != "STT_FUNC":
                continue
            code = data[s["st_value"]: s["st_value"] + s["st_size"]]
            addr, size, lvl = info[name]
            r = read(lvl, addr, size)
            pad = size - len(code)
            if 0 < pad <= 12 and not any(r[len(code):]):
                r = r[:len(code)]
            if len(code) == len(r) and mp.normalise(code) == mp.normalise(r):
                exact.setdefault(name, []).append(variant)
    out = AUTO / "exact"
    out.mkdir(exist_ok=True)
    for old in out.glob("*"):
        old.unlink()
    for name, vs in exact.items():
        v = vs[0]
        src = (AUTO / ("%s.%s.c" % (name, v))).read_text()
        extra = dict((a, c) for a, _, c in VARIANTS)[v]
        if extra:
            src = "/* cflags: %s */\n" % extra + src
        (out / (name + ".c")).write_text(src)
    print("tried %d functions, %d compile to exactly retail" % (len(tried), len(exact)))


def renumber(src):
    """Name the generated structures T1, T2 ... in order of appearance."""
    mapping = {}
    for m in re.finditer(r"\bS_\w+", src):
        mapping.setdefault(m.group(0), "Type%d" % (len(mapping) + 1))
    return re.sub(r"\bS_\w+", lambda m: mapping[m.group(0)], src)


def adopt():
    done = already_done()
    n = 0
    for f in sorted(glob.glob(str(AUTO / "exact" / "*.c"))):
        name = Path(f).name[:-2]
        if name in done:
            continue
        m = re.fullmatch(r"func_(L\d\d)_([0-9A-F]{8})", name)
        if m:
            dst = ROOT / "src" / "overlays" / m.group(1) / (m.group(2) + ".c")
        else:
            addr = int(name[5:], 16)
            sub = "core" if addr < 0x163B80 else "net" if addr >= 0x1E00000 else "game"
            dst = ROOT / "src" / sub / ("%08X.c" % addr)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(re.sub(r"\n{3,}", "\n\n", renumber(Path(f).read_text())).rstrip("\n") + "\n")
        n += 1
    print("adopted %d functions into src/" % n)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    cls = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else "overlay"
    if cmd == "prepare":
        n = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 300
        prepare(cls, n)
    elif cmd == "check":
        check(cls)
    elif cmd == "adopt":
        adopt()
    else:
        print(__doc__)
