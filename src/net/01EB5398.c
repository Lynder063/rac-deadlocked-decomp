#include "common.h"

s32 func_01E9C678(void *, void *, s32, s32);
extern s32 D_001694FC_[];
extern s32 D_1B26C0_[];
extern s32 D_1B2700_[];
#define D_001694FC (D_001694FC_[0])
#define D_1B26C0 (D_1B26C0_[0])
#define D_1B2700 (D_1B2700_[0])

void func_01EB5398(s32 a0) {
    if ((D_001694FC != 0) && (a0 >= 0)) {
        func_01E9C678(&D_1B26C0, &D_1B2700, a0, 0x1F4);
    }
}
