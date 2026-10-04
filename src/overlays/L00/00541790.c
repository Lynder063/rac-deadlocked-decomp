#include "common.h"

extern s32 D_00477198_[];
extern s32 D_0047719C_[];
extern s32 D_004771A0_[];
extern u32 D_004A31D0_[];
#define D_00477198 (D_00477198_[0])
#define D_0047719C (D_0047719C_[0])
#define D_004771A0 (D_004771A0_[0])
#define D_004A31D0 (D_004A31D0_[0])

s32 func_L00_00541790(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    if (arg0 < (u32) D_004A31D0) {
        D_004A31D0 = arg0;
        D_004771A0 = arg1;
        D_00477198 = arg2;
        D_0047719C = arg3;
    }
    return 0;
}
