/* Not matching yet: register choice differs for the multiply (tools/diff_func.py func_0054A810). Not part of the build. */
#include "common.h"

extern void func_0054A7E0(void);

u8 func_0054A810(char *base, s32 i) {
    func_0054A7E0();
    return *(u8 *)(base + i * 0x44 + 0xA40);
}
