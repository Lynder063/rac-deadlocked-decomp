/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00448350(s32);
s32 func_00458670();
s32 func_004E7830(s32);
extern s32 D_0021DE6C_[];
#define D_0021DE6C (D_0021DE6C_[0])

void func_004BAD50(s32 a0) {
    D_0021DE6C = a0;
    func_004E7830(1);
    func_00458670();
    func_00448350(0);
}
