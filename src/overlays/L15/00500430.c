#include "common.h"

s32 func_005004E0();
s32 func_L01_0052E4F0();
extern s32 D_0023C170_[];
#define D_0023C170 (D_0023C170_[0])

void func_L15_00500430(void) {
    switch (D_0023C170) {
    case 0:
        func_L01_0052E4F0();
        return;
    case 1:
        func_005004E0();
        break;
    }
}
