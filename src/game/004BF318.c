#include "common.h"

extern s32 func_004BF3A8(void);
extern s32 func_004BF4F0(void);
extern s32 func_004BF658(void);
extern s32 func_004BF7D8(void);
extern s32 func_004BF8E0(void);
extern s32 func_004BF718();

s32 func_004BF318(void) {
    s32 r;

    r = func_004BF8E0();
    if (r == -1) {
        r = func_004BF7D8();
        if (r == -1) {
            r = func_004BF718();
            if (r == -1) {
                r = func_004BF658();
                if (r == -1) {
                    r = func_004BF4F0();
                    if (r == -1) {
                        r = func_004BF3A8();
                    }
                }
            }
        }
    }
    return (r == -1) ? 0 : r;
}
