/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00498100();
s32 func_00498120(s32);
s32 func_00498158(s32, s32);
s32 func_00510BE8(s32);
s32 func_00522868(s32, s32);

s32 func_004981F8(s32 a0, s32 a1) {
    if (func_00498100() == 0) {
        if ((a1 != func_00498120(a0)) && (func_00498158(a0, a1) != 0)) {
            func_00522868(func_00510BE8(a0), a1);
            return 1;
        }
        return 0;
    }
    return 0;
}
