/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L01_004D8DD8();

s32 func_L01_004D8DE8(void) {
    return (func_L01_004D8DD8() ^ 1) & 0xFF;
}
