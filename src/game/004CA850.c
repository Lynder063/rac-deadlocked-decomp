/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0049B208(s32);
s32 func_004CA818();
extern s32 D_0021EEB4_[];
#define D_0021EEB4 (D_0021EEB4_[0])

void func_004CA850(void) {
    if (D_0021EEB4 != 0) {
        func_004CA818();
        return;
    }
    func_0049B208(0);
}
