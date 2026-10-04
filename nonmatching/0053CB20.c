/* Not matching yet (tools/diff_func.py func_0053CB20). Not part of the build. */
#include "common.h"

typedef struct Buf {
    char pad0[0x54];
    u8 used;
} Buf;

extern void func_00453718(s32 a, void *b);

void func_0053CB20(Buf *b, s32 a, s32 n) {
    func_00453718(a, (char *)b + (b->used + 0xC));
    b->used = b->used + n;
}
