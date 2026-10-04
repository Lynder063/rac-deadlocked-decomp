/* cflags: -mno-split-addresses */
#include "common.h"

f32 func_L00_005BCE18();
s32 func_L00_005BD140(s32, s32, f32);

void func_L01_005A0158(s32 arg0, s32 arg1) {
    func_L00_005BD140(arg0, arg1, (func_L00_005BCE18() * 0.5f) + 0.5f);
}
