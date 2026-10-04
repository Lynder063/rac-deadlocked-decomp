#include "common.h"

void func_004A46A8(void);
void func_004A47A0(void);
void func_004A4880(void);
void func_004A49E0(void);
void func_004A4BC0(void);
s32 func_00505B20(void);

extern s32 D_307B58_[];
#define D_307B58 (D_307B58_[0])

void func_004A45F8(s32 a0) {
    s32 *temp_s0;

    temp_s0 = (func_00505B20() * 0xEC) + &D_307B58;
    if (*temp_s0 & 1) {
        func_004A46A8();
    }
    if (*temp_s0 & 2) {
        func_004A47A0();
    }
    if (*temp_s0 & 4) {
        func_004A4880();
    }
    if (*temp_s0 & 8) {
        func_004A49E0();
    }
    if (*temp_s0 & 0x10) {
        func_004A4BC0();
    }
}
