#include "common.h"

extern void func_004B8B88(void);
extern s32 func_00505B20(void);
extern s32 func_005014B0(s32 a0);
/* Declared without a size so it is addressed with lui, not $gp (-G8). */
extern s32 D_0030A160_[];

void func_004B80D0(s32 a0) {
    s32 *p;
    s32 t;

    p = &D_0030A160_[func_00505B20() * 4];
    t = *p;
    switch (t) {
    case 1:
        *p = 0;
        return;
    case 2:
        func_005014B0(a0);
        break;
    case 0:
        func_004B8B88();
        break;
    }
}
