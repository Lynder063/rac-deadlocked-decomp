/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0011A518(s32, s32, s32);
s32 func_0011AB04(s32);
s32 func_0011AFC8(s32, s32, s32);

void func_L00_00710D68(s32 arg0, s32 arg1) {
    s32 temp_s0;
    s32 temp_v0;

    if (arg1 != 0) {
        temp_s0 = arg0 + 0x18;
        func_0011A518(temp_s0, 0, 0x34);
        temp_v0 = func_0011AB04(arg1);
        func_0011AFC8(temp_s0, arg1, (temp_v0 < 0x35) ? temp_v0 : 0x34);
    }
}
