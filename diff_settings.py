# asm-differ configuration. asm-differ itself is cloned locally, not
# vendored:  git clone https://github.com/simonlindholm/asm-differ tools/ext/asm-differ
#
# Binary mode over flattened images, because our build is one linked ELF
# rather than one object per function. Regenerate the images after every
# link with tools/gen_differ_files.py (sh tools/diff.sh FUNC does build+link+regen+diff).
# objdump is a rabbitizer shim: the SN toolchain's ee-objdump has no -z and
# hides zero words, i.e. exactly the nops we are usually diffing.

def apply(config, args):
    config["baseimg"] = "build-sn/differ_base.bin"
    config["myimg"] = "build-sn/differ_my.bin"
    config["mapfile"] = "build-sn/differ.map"
    config["source_directories"] = ["src", "include"]
    config["arch"] = "mipsee"
    config["map_format"] = "gnu"
    import os
    if os.name == "nt":
        # Absolute, backslashed path: CreateProcess won't resolve a relative
        # forward-slash path to a .bat.
        config["objdump_executable"] = os.path.abspath(os.path.join("tools", "objdump_shim.bat"))
    else:
        config["objdump_executable"] = os.path.abspath(os.path.join("tools", "objdump_shim.py"))
