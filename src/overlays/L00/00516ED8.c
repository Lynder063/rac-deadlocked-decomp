#include "common.h"

s32 func_L00_0053A4C0(void *);
extern s32 D_0049E954_[];
extern s32 D_004AD138_[];
#define D_0049E954 (D_0049E954_[0])
#define D_004AD138 (D_004AD138_[0])

s32 func_L00_00516ED8(void) {
    if (D_0049E954 != 0) {
        D_0049E954 = 0;
        func_L00_0053A4C0(&D_004AD138);
    }
    return 0;
}
