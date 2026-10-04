#include "common.h"

typedef struct SFile {
    char pad0[0xE];
    s16 h;
    char pad10[0x44];
    s32 fd;
} SFile;

extern s32 func_0011BF88(s32 a, s32 b);
extern s32 func_0011C2D8(void *);
extern void func_0011D3E8(void *r, s32 (*fn)(void *));

void func_0011C950(void *r) {
    func_0011D3E8(r, func_0011C2D8);
}

s32 func_0011DB90(SFile *p) {
    return func_0011BF88(p->fd, p->h);
}
