/* cflags: -mno-split-addresses */
#include "common.h"

typedef struct Type1 Type1;

struct Type1 {
    void * * f0;
    void * * f4;
    void * * f8;
    s8 * fC;
    s8 * f10;
    s8 * f14;
    s8 * f18;
    s8 * f1C;
    s8 * f20;
    s8 f24;
    s8 f28;
    s8 f2C;
    s8 f30;
    s8 f34;
    s16 f38;
    s16 f3A;
    s8 f3C;
    s8 f40;
    s8 f44;
    s8 f48;
    s8 f4C;
    s8 f50;
    s32 f54;
    void * * f58;
    s16 f5C;
    s16 f5E;
    s16 f60;
    char _p62[0x2];
    s32 f64;
    s32 f68;
    u32 f6C[2];
};

void **func_01EF0A58(s8 *);
s32 func_01EF0D18();

void func_01EF0C1C(Type1 *a0) {
    if (func_01EF0D18() != 0) {
        a0->f4 = func_01EF0A58(a0->fC);
    }
}
