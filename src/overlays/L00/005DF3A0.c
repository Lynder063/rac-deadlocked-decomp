#include "common.h"

s32 func_L00_005DE2A8();
s32 func_L00_006790B0(s32);
extern s32 D_0026C8A8_[];
#define D_0026C8A8 (D_0026C8A8_[0])

void func_L00_005DF3A0(void) {
    if (D_0026C8A8 != 0) {
        func_L00_006790B0(0x10);
        func_L00_005DE2A8();
    }
}
