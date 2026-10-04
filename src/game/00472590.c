/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00163408();

s32 func_00472590(s32 a0, s32 a1) {
    return (func_00163408() % (s32) ((a1 - a0) + 1)) + a0;
}
