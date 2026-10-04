/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005288B8(u8 *arg0) {
    u8 temp_v1;

    temp_v1 = *arg0;
    return ((temp_v1 >> 4) * 0xA) + (temp_v1 & 0xF);
}
