#include "common.h"

s32 func_0011D920(s32, void *, s32, s32);
extern s32 D_00221900_[];
#define D_00221900 (D_00221900_[0])

void func_L00_0077A600(s32 arg0, s32 arg1) {
    func_0011D920(arg1, &D_00221900, arg0 / 60, arg0 % 60);
}
