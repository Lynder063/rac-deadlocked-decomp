/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00163408();

f32 func_004725D8(f32 a0, f32 a1) {
    return a0 + ((f32) func_00163408() * (a1 - a0) * 0.000030517578f);
}
