/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00526DC0(s32 a0, s32 a1);
void func_00526FD8(s32 a0, s32 a1, s32 a2);

void func_00522A30(s32 a0, s32 a1) {
    if (a1 == 8) {
        if (func_00526DC0(a0, 0xD) == 0) {
            func_00526DC0(a0, 0xE);
        }
    }
    func_00526FD8(a0, 0xD, 0xE);
    if ((a1 == 0x11) && (func_00526DC0(a0, 0x1E) == 0)) {
        func_00526DC0(a0, 0x1F);
    }
    func_00526FD8(a0, 0x1E, 0x1F);
    if ((a1 == 5) && (func_00526DC0(a0, 0x26) == 0)) {
        func_00526DC0(a0, 0x27);
    }
    func_00526FD8(a0, 0x26, 0x27);
}
