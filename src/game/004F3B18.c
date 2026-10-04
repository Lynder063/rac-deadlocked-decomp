#include "common.h"

void func_004DEDD8(void);
void func_004DEEF8(void);
void func_004DEF78(void);
void func_004E7990(u32 a0, u64 a1, s32 a2);

extern s32 D_1DFCF8_[];
#define D_1DFCF8 (D_1DFCF8_[0])

void func_004F3B18(void) {
    func_004DEEF8();
    func_004DEDD8();
    func_004DEF78();
    func_004E7990(0x47U, 0x5360BU, 0);
    func_004E7990(0x4EU, 0x01000000 | ((s32) D_1DFCF8 >> 0xD), 0);
}
