#include "common.h"

s32 func_0047D520();
extern u8 D_26F430_[];
#define D_26F430 (D_26F430_[0])

s32 func_0047D4E8(void) {
    if (D_26F430 == 0) {
        func_0047D520();
    }
    return (s32) &D_26F430;
}
