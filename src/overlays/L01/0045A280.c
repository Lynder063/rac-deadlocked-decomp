/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005E60A0(s32);
s32 func_L01_00591BD8(s32, s32, s32);

void func_L01_0045A280(s32 arg0) {
    if (func_L00_005E60A0(6) == 0) {
        func_L01_00591BD8(arg0, 4, -1);
        return;
    }
    func_L01_00591BD8(arg0, 5, -1);
}
