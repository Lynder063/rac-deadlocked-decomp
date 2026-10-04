/* cflags: -mno-split-addresses */
#include "common.h"

typedef union Type1 Type1;
typedef struct Type2 Type2;
typedef struct Type3 Type3;
typedef struct Type4 Type4;
typedef struct Type5 Type5;
typedef struct Type6 Type6;
typedef struct Type7 Type7;

union Type1 {
    void * f0;
};

struct Type2 {
    Type1 f0;
    char f4[0xC24];
};

struct Type3 {
    u8 f0;
    Type2 f4[4];
};

struct Type4 {
    s32 f0;
    s32 f4;
    Type3 f8;
};

struct Type5 {
    u32 f0;
    u32 f4;
    u32 f8;
    u32 fC;
    u32 f10;
    u32 f14;
    u32 f18;
    u32 f1C;
    u32 f20;
    u32 f24;
    u32 f28;
    u32 f2C;
    u32 f30;
    u32 f34;
    u32 f38;
    u32 f3C;
    u32 f40;
    u32 f44;
    u32 f48;
    u32 f4C;
    u32 f50;
    u32 f54;
    u32 f58;
    u32 f5C;
    u32 f60;
    u32 f64;
};

struct Type6 {
    s32 f0;
    char _p15[0x3];
    s32 f18;
    s32 f1C;
    s32 f20;
    s32 f40;
    s32 f44;
    s32 f64;
    Type5 f164;
};

struct Type7 {
    Type4 f0;
    s8 f68;
    s8 f69;
    u16 f6A;
    s8 f6C;
    s8 f6D;
    s16 f6E;
    f32 f70;
    u16 f74;
    s8 f76;
    s8 f77;
    f32 f78;
    f32 f7C;
    Type4 f80;
    char _pE8[0x8];
    Type6 fF0;
};

u32 func_0048A170();
s32 func_0048A290(s32, u32);

u32 func_0048A120(s32 a0, s32 a1, s32 a2, Type7 *a3, u32 a4) {
    u32 temp_v0;

    temp_v0 = func_0048A170();
    if (temp_v0 != 0xFFFFFFFF) {
        func_0048A290(a0, temp_v0);
    }
    return temp_v0;
}
