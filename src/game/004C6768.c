#include "common.h"

extern s32 func_004C67D8(void);
extern s32 func_004C6970(void);
extern s32 func_004C6AE0(void);
extern s32 func_004C6BA0(void);
extern s32 func_004C6CC0(void);

s32 func_004C6768(void) {
    s32 r;

    r = func_004C6AE0();
    if (r == -1) {
        if (func_004C67D8() != 0) {
            r = func_004C6BA0();
            if (r == -1) {
                r = func_004C6CC0();
            }
        } else {
            r = func_004C6970();
        }
    }
    return (r == -1) ? 0 : r;
}
