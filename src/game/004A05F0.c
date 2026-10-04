/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0049C620(s32, s32);
s32 func_0049D430(s32, s32);
s32 func_0049E048(s32, s32);
s32 func_0049F040(s32, s32);
s32 func_004A0220(s32, s32);
s32 func_00505B20();
s32 func_00505B70(s32, s32);
s32 func_00506B70(s32);

void func_004A05F0(void) {
    s32 temp_s0;

    temp_s0 = func_00505B20();
    func_00506B70(0x100000);
    func_0049C620(0x100000, temp_s0);
    func_00505B70(0x15, 0x100000);
    func_00506B70(0x110000);
    func_0049D430(0x110000, temp_s0);
    func_00505B70(0xE, 0x110000);
    func_00506B70(0x120000);
    func_0049E048(0x120000, temp_s0);
    func_00505B70(0x13, 0x120000);
    func_00506B70(0x130000);
    func_0049F040(0x130000, temp_s0);
    func_00505B70(0x14, 0x130000);
    func_00506B70(0x140000);
    func_004A0220(0x140000, temp_s0);
    func_00505B70(0x12, 0x140000);
}
