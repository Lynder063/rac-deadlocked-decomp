#include "common.h"

typedef struct Entry1A4 {
    s32 f0;
    s32 f4;
    s32 f8;
    char pad[0x198];
} Entry1A4;

extern Entry1A4 D_0031A960[];
extern s32 func_00505B20(void);

void func_004D0AC8(void) {
    Entry1A4 *e = &D_0031A960[func_00505B20()];
    e->f8 = e->f8 & ~1;
}
