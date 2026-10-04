/* Not matching yet (tools/diff_func.py func_004F3B18). Not part of the build. */
#include "common.h"

extern s32 D_001DFCF8[];
#define D_001DFCF8 (D_001DFCF8[0])
extern void func_004DEDD8(void);
extern void func_004DEEF8(void);
extern void func_004DEF78(void);
extern void func_004E7990(s32 a, s32 b, s32 c);

void func_004F3B18(void) {
    func_004DEEF8();
    func_004DEDD8();
    func_004DEF78();
    func_004E7990(0x47, 0x5360B, 0);
    func_004E7990(0x4E, 0x01000000 | (D_001DFCF8 >> 13), 0);
}
