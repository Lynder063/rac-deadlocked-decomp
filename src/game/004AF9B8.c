#include "common.h"

extern void func_0049A6B0(s32 a, s32 b);
extern void func_004AFA18(void);
extern s32 func_00505B20(void);

void func_004AF9B8(void) {
    func_004AFA18();
    func_0049A6B0(func_00505B20(), 0x100);
}
