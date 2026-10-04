/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00504238(u32 a0, f32 a1, f32 a2);

s32 func_005058E0(u32, f32, f32);

s32 func_00504840(u32 a0, f32 a1, f32 a2, f32 a3, f32 a4) {
    f32 temp_f20;
    f32 temp_f21;

    temp_f21 = a3 - a1;
    temp_f20 = a4 - a2;
    if (func_00504238(a0, a1 + (temp_f21 * 0.5f), a2 + (temp_f20 * 0.5f)) != 0) {
        func_005058E0(a0, temp_f21, temp_f20);
    }
    return 0;
}
