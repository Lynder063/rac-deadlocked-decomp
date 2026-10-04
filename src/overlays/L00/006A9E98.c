/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_006AA3D0();
s32 func_L00_006AAE40();
s32 func_L00_006EBFE8();
s32 func_L00_006F4418();
s32 func_L00_006F6E68();
s32 func_L00_006F9558();
extern s32 D_0021E6B4_[];
#define D_0021E6B4 (D_0021E6B4_[0])

void func_L00_006A9E98(void) {
    func_L00_006EBFE8();
    func_L00_006F4418();
    func_L00_006F6E68();
    func_L00_006AAE40();
    func_L00_006AA3D0();
    if (D_0021E6B4 == 1) {
        func_L00_006F9558();
    }
}
