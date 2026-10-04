/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00502410(u32 *a0, u32 a1) {
    return (a0[a1 & 0xFFFFFFF8] & (1 << (a1 & 7))) != 0;
}
