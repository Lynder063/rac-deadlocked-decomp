#include "common.h"

f32 func_L01_00652E38(s32 arg0) {
    s32 temp_v0;

    temp_v0 = (arg0 << 0xD) ^ arg0;
    return 1.0f - ((f32) (((temp_v0 * ((temp_v0 * temp_v0 * 0x3D73) + 0xC0AE5)) + 0x5208DD0D) & 0x7FFFFFFF) * 9.313226e-10f);
}
