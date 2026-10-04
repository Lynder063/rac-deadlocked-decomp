#include "common.h"

void func_00163960(u32 r, u64 ud) {
    s32 *q = ((s32 **)ud)[1];
    if (r) {
        *q = r;
    } else {
        *q = 0;
    }
}
