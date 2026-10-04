#!/usr/bin/env python3
"""
Add the nops retail's assembler added, to compiled game code.

Retail's text segment was assembled by SN Systems' own ps2eeas, not the
GNU as this build uses, and ps2eeas inserts nops GNU as does not.
core_text was assembled by the same GNU as the build runs (the compiler
driver's ee/bin/as.exe), so this runs on src/game/ objects, plus
989snd.o, whose retail code has ps2eeas's short-loop padding on loops
with calls (func_0012E688, func_0012EC60). Three rules:

1. Short loops (the R5900 short-loop erratum). Every backward branch
   whose loop -- the target through the branch itself -- is shorter than
   six instructions gets nops right before the branch until it is
   exactly six. Measured on ps2eeas directly (tools in the toolchain
   mirrors): in reorder and noreorder code alike, branch-likely too,
   counting any other instructions in the loop, delay slots included.
   This is why 309 of retail's backward branches span exactly six
   instructions. The driver's as.exe already pads loops that contain no
   call, in the first-pass object this measures, so in effect this adds
   the padding ps2eeas also gives loops with a call.

   The driver's as.exe measures differently, though: it counts from the
   target label to the first jump after it, not to the branch. On a
   backward branch that is not a loop -- a cross-jump back into a short
   block that returns -- it pads where ps2eeas did not (func_00209188:
   three nops). Where GNU as gave a branch more nops than ps2eeas's rule,
   the branch is written as a `.word` with its offset computed from the
   label, which GNU as cannot pad, and gets ps2eeas's padding instead.
   Only branches in the compiler's noreorder blocks, whose delay slot is
   spelled out, are rewritten.

2. FP compare then branch. A `c.cond.fmt` immediately followed by a
   `bc1*` gets a nop between them. In retail text the pair is never
   adjacent (191 of 191 have the nop). GNU as adds one on its own in
   some contexts and not in others (not when the compiler leaves an
   unfilled bc1 in reorder mode), so the pairs are found in the
   assembled object, never guessed from the source.

3. GPR to FPU move. An `mtc1 $x, $fN` -- written out or from an `li.s`
   expansion -- immediately followed by an instruction that reads $fN
   gets a nop between them, in reorder code (215 times in retail text;
   the 17 adjacent pairs are all in hand-written noreorder code). GNU
   as never adds this one. Sites must be found alike in the object and in
   the source, or the tool refuses to guess. fastfunc.o is skipped: its
   retail code is hand-written noreorder assembly (every mtc1 there is
   directly followed by its reader), even where our C reproduces it.

ps2eeas itself cannot be used here: it recurses without end on some of
the retail stubs that INCLUDE_ASM feeds it, and it has no -G small-data
expansion (docs/DECOMP_PROGRESS.md).

Two passes, so that nothing is guessed about macro expansion or delay
slots: IN.o is IN.s assembled. Everything is measured in it, per compiled
function (the INCLUDE_ASM stubs are retail's bytes and already padded),
and the nops go into IN.s before the matching branch. A loop's span
counts the FP nops inserted inside it.

usage: python tools/ps2eeas_nops.py IN.s IN.o OUT.s
"""
import re
import sys

import rabbitizer as rz
from elftools.elf.elffile import ELFFile

MIN_SPAN = 5   # target through the branch, not counting its own delay slot (6 with it)
# Objects whose retail code is hand-written noreorder assembly: none known here yet.
NOREORDER_OBJECTS = set()


def noreorder_ranges():
    """[(start, end)] of retail's hand-written noreorder objects in text."""
    return []


BRANCH_LINE = re.compile(r"^\s*(b[a-z0-9]*)\s+(.*)$")
BC1_LINE = re.compile(r"^\s*bc1(t|f)l?\s")


def is_local_branch(mnemonic: str, operands: str) -> bool:
    """A conditional or unconditional branch to a local label: what closes a
    loop in compiled code. (`break` also starts with b; its operands are
    numbers, so it never qualifies.)"""
    target = operands.split(",")[-1].strip()
    return target.startswith(("$L", ".L"))


def decode(text, addr):
    return rz.Instruction(int.from_bytes(text[addr:addr + 4], "little"), vram=addr,
                          category=rz.InstrCategory.R5900)


def reads_fpr(mnemonic: str, operands: str, reg: str) -> bool:
    """Does this instruction read FP register REG? Normally the first
    operand is the destination; compares, stores (swc1, or s.s as the
    compiler writes them), moves out of the FPU and the accumulator ops
    (adda.s ...) read all of theirs."""
    parts = [o.strip() for o in operands.split(",")]
    used = re.compile(re.escape(reg) + r"(?![0-9])")
    if (mnemonic.startswith("c.") or mnemonic in ("swc1", "s.s", "mfc1")
            or re.match(r"(adda|suba|mula|madda|msuba)\.s$", mnemonic)):
        return any(used.search(p) for p in parts)
    return any(used.search(p) for p in parts[1:])


def scan(start, size, text):
    """(backward, fp, moves) for one function: backward is [(target,
    branch)] for every backward branch in order; fp is [(address,
    needs_nop)] for every bc1 in order, needs_nop when the instruction
    before it is an FP compare; moves is the address of every instruction
    that reads the FP register an mtc1 right before it wrote (the mtc1
    not in a delay slot)."""
    backward, fp, moves = [], [], []
    prev = before = None
    for addr in range(start, start + size, 4):
        ins = decode(text, addr)
        name = ins.getOpcodeName()
        if name.startswith("bc1"):
            fp.append((addr, prev is not None and prev.getOpcodeName().startswith("c.")))
        if prev is not None and prev.getOpcodeName() == "mtc1" \
                and not (before is not None and (before.isBranch() or before.isJump())):
            reg = prev.disassemble().split(",")[-1].strip()
            if reads_fpr(name, ins.disassemble().split(None, 1)[-1], reg):
                moves.append(addr)
        if ins.isBranch():
            target = ins.getBranchVramGeneric()
            if target <= addr:
                backward.append((target, addr))
        before, prev = prev, ins
    return backward, fp, moves


INSN_LINE = re.compile(r"^\s*([a-z][a-z0-9.]*)\s*(.*?)\s*(#.*)?$")


def gnu_padding(text, start, branch, lines, j):
    """Nops GNU as put right before the branch at BRANCH (source line J):
    the object's run of nops there, not counting a delay slot, less the
    nops the source itself writes there."""
    run, a = 0, branch - 4
    while a >= start and text[a:a + 4] == b"\0\0\0\0":
        if a - 4 >= start:
            prev = decode(text, a - 4)
            if prev.isBranch() or prev.isJump():
                break
        run += 1
        a -= 4
    # A bc1's nop after its FP compare is the hazard nop (rule 2), which
    # ps2eeas has too.
    if run and a >= start and decode(text, branch).getOpcodeName().startswith("bc1") \
            and decode(text, a).getOpcodeName().startswith("c."):
        run -= 1
    written, k = 0, j - 1
    while k >= 0:
        stripped = lines[k].split("#")[0].strip()
        if not stripped or stripped.startswith(".") or stripped.endswith(":"):
            k -= 1
        elif stripped == "nop":
            written += 1
            k -= 1
        else:
            break
    return max(0, run - written)


REGS = {"$zero": 0, "$at": 1, "$gp": 28, "$sp": 29, "$fp": 30, "$ra": 31}
# op -> (primary opcode, operands: s = rs, t = rt, a digit = REGIMM's rt code)
BRANCHES = {
    "b": (0x04, ""), "beq": (0x04, "st"), "bne": (0x05, "st"),
    "beql": (0x14, "st"), "bnel": (0x15, "st"),
    "beqz": (0x04, "s"), "bnez": (0x05, "s"), "beqzl": (0x14, "s"), "bnezl": (0x15, "s"),
    "blez": (0x06, "s"), "bgtz": (0x07, "s"), "blezl": (0x16, "s"), "bgtzl": (0x17, "s"),
    "bltz": (0x01, "s0"), "bgez": (0x01, "s1"), "bltzl": (0x01, "s2"), "bgezl": (0x01, "s3"),
}


def branch_as_word(line):
    """LINE, a branch to a local label, as a `.word` that encodes it, or
    None for a form not handled here."""
    m = re.match(r"^(\s*)([a-z]+)\s+([^#]*?)\s*(#.*)?$", line.rstrip("\n"))
    if not m or m.group(2) not in BRANCHES:
        return None
    opcode, shape = BRANCHES[m.group(2)]
    ops = [o.strip() for o in m.group(3).split(",")]
    label, regs = ops[-1], ops[:-1]

    def reg(r):
        return REGS[r] if r in REGS else int(r[1:])
    word = opcode << 26
    if shape.startswith("s"):
        word |= reg(regs[0]) << 21
    if shape == "st":
        word |= reg(regs[1]) << 16
    elif shape[1:]:
        word |= int(shape[1:]) << 16
    return f"{m.group(1)}.word\t{word:#010x} | ((({label} - . - 4) >> 2) & 0xFFFF)\n"


EXTERN = re.compile(r"^\s*\.extern\s+(\w+)\s*,\s*(\d+)")
SMALL = 2           # -G2: an object this size or smaller is $gp-relative, one instruction


def macro_access(lines, operands: str) -> bool:
    """A load or store to a bare symbol the assembler expands to `lui $at`
    plus the access (a global bigger than SMALL, or undeclared): the lui
    then sits between the mtc1 and the read, so there is no hazard. A
    $gp-relative one (an `__gp` alias, a small object) stays adjacent."""
    target = operands.split(",")[-1].strip()
    if "(" in target or not re.match(r"^[A-Za-z_][\w.]*(\s*[+-]\s*\w+)?$", target):
        return False
    sym = re.split(r"\s*[+-]", target)[0]
    if sym.endswith("__gp"):
        return False
    sizes = {m.group(1): int(m.group(2)) for l in lines if (m := EXTERN.match(l))}
    return sizes.get(sym, SMALL + 1) > SMALL


def move_sites(lines, start, end):
    """Source lines that read the FP register a reorder-mode `mtc1`/`li.s`
    on the previous instruction line wrote; the nop goes before them. A
    macro access to a large global is not one (macro_access())."""
    sites, reorder, pending = [], True, None
    for j in range(start, end):
        stripped = lines[j].strip()
        if stripped in (".set\tnoreorder", ".set noreorder"):
            reorder, pending = False, None
            continue
        if stripped in (".set\treorder", ".set reorder"):
            reorder, pending = True, None
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":") and not stripped.startswith("."):
            continue        # a label reached by fallthrough: the read after it still counts, as in scan()
        m = INSN_LINE.match(stripped)
        if not m or stripped.startswith("."):
            pending = None
            continue
        mnemonic, operands = m.group(1), m.group(2)
        if pending and reads_fpr(mnemonic, operands, pending) and not macro_access(lines, operands):
            sites.append(j)
        pending = None
        if reorder and mnemonic in ("mtc1", "li.s"):
            pending = operands.split(",")[1 if mnemonic == "mtc1" else 0].strip()
    return sites


def main() -> None:
    src_path, obj_path, dst_path = sys.argv[1:4]
    lines = open(src_path).readlines()
    elf = ELFFile(open(obj_path, "rb"))
    text = elf.get_section_by_name(".text").data()
    tidx = next(i for i, s in enumerate(elf.iter_sections()) if s.name == ".text")
    funcs = {s.name: (s["st_value"], s["st_size"])
             for s in elf.get_section_by_name(".symtab").iter_symbols()
             if s["st_shndx"] == tidx and s["st_info"]["type"] == "STT_FUNC" and s["st_size"]}

    inserts = {}  # line index -> number of nops to put before it
    as_words = set()  # branch lines to write as .word (GNU as over-padded them)
    loops = fps = moves = 0
    hand_written = noreorder_ranges()
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*\.ent\s+(\S+)", lines[i])
        if not m or m.group(1) not in funcs:
            i += 1
            continue
        name = m.group(1)
        end = next(j for j in range(i, len(lines)) if re.match(rf"^\s*\.end\s+{re.escape(name)}\s*$", lines[j]))
        # Backward branches only: a loop closes backward, and the assembler's
        # own macro branches (the div-by-zero trap guard) all jump forward,
        # so pairing the backward ones keeps source and object one to one.
        # bc1 branches are never macro-generated, so all of them pair.
        seen, src_back, src_bc1 = set(), [], []
        for j in range(i, end):
            lm = re.match(r"^\s*(\$L\w+|\.L\w+):", lines[j])
            if lm:
                seen.add(lm.group(1))
            if BC1_LINE.match(lines[j]):
                src_bc1.append(j)
            bm = BRANCH_LINE.match(lines[j])
            if bm and is_local_branch(bm.group(1), bm.group(2)) \
                    and bm.group(2).split(",")[-1].strip() in seen:
                src_back.append(j)
        start, size = funcs[name]
        obj_back, obj_fp, obj_moves = scan(start, size, text)
        src_moves = move_sites(lines, i, end)
        vram = int(name[5:], 16) if re.fullmatch(r"func_[0-9A-Fa-f]{8}", name) else None
        if vram is not None and any(a <= vram < b for a, b in hand_written):
            obj_moves, src_moves = [], []
        if len(obj_back) != len(src_back) or len(obj_fp) != len(src_bc1) \
                or len(obj_moves) != len(src_moves):
            sys.exit(f"ps2eeas_nops: {name}: object has {len(obj_back)} backward branches, "
                     f"{len(obj_fp)} bc1, {len(obj_moves)} mtc1 uses; source has "
                     f"{len(src_back)}, {len(src_bc1)}, {len(src_moves)} -- refusing to guess")
        fp_nops = [addr for addr, needs in obj_fp if needs] + obj_moves
        for (addr, needs), j in zip(obj_fp, src_bc1):
            if needs:
                inserts[j] = inserts.get(j, 0) + 1
                fps += 1
        for j in src_moves:
            inserts[j] = inserts.get(j, 0) + 1
            moves += 1
        for (target, branch), j in zip(obj_back, src_back):
            span = (branch - target) // 4 + 1 + sum(1 for a in fp_nops if target <= a <= branch)
            gnu = gnu_padding(text, start, branch, lines, j)
            need = max(0, MIN_SPAN - (span - gnu))
            if gnu > need:
                as_words.add(j)
                if need:
                    inserts[j] = inserts.get(j, 0) + need
                    loops += 1
            elif span < MIN_SPAN:
                inserts[j] = inserts.get(j, 0) + MIN_SPAN - span
                loops += 1
        i = end + 1

    out, reorder = [], True
    for j, line in enumerate(lines):
        if j in inserts:
            nops = ["\tnop\n"] * inserts[j]
            if reorder:
                # Make the assembler keep them as written; the branch itself
                # stays in reorder mode.
                nops = ["\t.set\tnoreorder\n"] + nops + ["\t.set\treorder\n"]
            # Inside the compiler's own .set noreorder block (the usual case:
            # the branch and its delay slot are spelled out) plain nops keep
            # the branch and its delay slot exactly as they were.
            out += nops
        stripped = line.strip()
        if stripped == ".set\tnoreorder" or stripped == ".set noreorder":
            reorder = False
        elif stripped == ".set\treorder" or stripped == ".set reorder":
            reorder = True
        if j in as_words:
            word = branch_as_word(line) if not reorder else None
            if word is None:
                sys.exit(f"ps2eeas_nops: {src_path}:{j + 1}: GNU as pads this branch more "
                         f"than ps2eeas did, and it cannot be written as a .word here: {stripped}")
            line = word
        out.append(line)
    open(dst_path, "w").writelines(out)
    print(f"ps2eeas_nops: padded {loops} short loop(s), {fps} FP compare(s), "
          f"{moves} mtc1 use(s), unpadded {len(as_words)} branch(es) {src_path} -> {dst_path}")


if __name__ == "__main__":
    main()
