/* cflags: -mno-split-addresses */
#include "common.h"

f32 func_00473B10(f32 a0, f32 a1, f32 a2, f32 a3, f32 a4) {
    f32 temp_f0;
    f32 temp_f1;
    f32 temp_f3;

    temp_f1 = a0 - a1;
    temp_f3 = a4 * a4;
    temp_f0 = (a3 - a2) - temp_f1;
    return (temp_f0 * (temp_f3 * a4)) + ((temp_f1 - temp_f0) * temp_f3) + ((a2 - a0) * a4) + a1;
}
