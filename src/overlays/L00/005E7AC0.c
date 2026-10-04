/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005E7AC0(s32 *arg0, s32 arg1) {
    s32 temp_a2;
    s32 temp_v0;
    s32 temp_v0_2;

    temp_a2 = *arg0;
    temp_v0_2 = (temp_a2 >> 0x18) - arg1;
    temp_v0 = (temp_v0_2 <= -1) ? 0 : temp_v0_2;
    *arg0 = (temp_a2 & 0xFFFFFF) | (temp_v0 << 0x18);
    return temp_v0 == 0;
}
