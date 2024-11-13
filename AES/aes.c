#include "aes.h"

#define MUL2(a) (a<<1)^(a&0x80?0x1b:0)
#define MUL3(a) (MUL2(a))^(a)
#define MUL4(a) MUL2((MUL2(a)))
#define MUL8(a) MUL2((MUL2((MUL2(a)))))
#define MUL9(a) (MUL8(a))^(a)
#define MULB(a) (MUL8(a))^(MUL2(a))^(a)
#define MULD(a) (MUL8(a))^(MUL4(a))^(a)
#define MULE(a) (MUL8(a))^(MUL4(a))^(MUL2(a))

u8 MUL(u8 a, u8 b) {
    u8 r = 0;
    u8 tmp = b;
    u32 i;
    for (i=0;i<8;i++){
        if (a & 1)r ^= tmp;
        tmp = MUL2(tmp);
        a >>= 1;
    }
    return r;

}

/*
At^(-1) xor b = At^(254) xor b -> t^(1111 1110)
*/
/*
    
    r = MUL(r, r); //a2
    r = MUL(r, a); //a3
    r = MUL(r, r); //a6
    r = MUL(r, a); //a7
    r = MUL(r, r); //a14
    r = MUL(r, a); //a15
    r = MUL(r, r); //a30
    r = MUL(r, a); //a31
    r = MUL(r, r); //a62
    r = MUL(r, a); //a63
    r = MUL(r, r); //a126
    r = MUL(r, a); //a127
    r = MUL(r, r); //a254
    
*/
u8 inv(u8 a) {
    u8 r = a;
    for (int i = 0; i<6; i++){
        r = MUL(r, r);
        r = MUL(r, a);
    }
    r = MUL(r, r);
    
    return r;
}

u8 GenSbox(u8 a) {
    u8 r = 0;
    u8 tmp;
    tmp = inv(a);
    if (tmp & 1) r ^= 0x1f;
    if (tmp & 2) r ^= 0x3e;
    if (tmp & 4) r ^= 0x7c;
    if (tmp & 8) r ^= 0xf8;
    if (tmp & 16) r ^= 0xf1;
    if (tmp & 32) r ^= 0xe3;
    if (tmp & 64) r ^= 0xc7;
    if (tmp & 128) r ^= 0x8f;
    return r ^ 0x63;    
}

u8 GenInvSbox(u8 a) {
    u8 r;
    r = a;
    






    return r;
}

void PrintSBox(){
    printf("Sbox[256]: \n");
    for (int i = 0; i<256;i++){
        printf("0x%02x, ",GenSbox((u8) i));
        if (i % 16 == 15) printf("\n");
    }
}

state AddRK(state s) {
    for (u8 i = 0; i < 4; i++) {
        for (u8 j = 0; j < 4; j++) {
            s.x[i][j] = GenSbox(s.x[i][j]);
        }
    }
    return s;
}

/*
void AES_ENC() {
    u8 tmp;
    u8 state = AddRK(tmp);
    int round;
    int ROUND; // Total number of Rounds for AES
    for (round = 1; round < ROUND-1; round++) {
        SubByte();
        ShiftRow();
        MixColumn();
        AddRK(tmp);
    }
    SubByte();
    ShiftRow();
    AddRK(tmp);
}*/

int main(){
    // u8 MK[32] = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};
    printf("%02x\n", GenSbox(0xc6));
    printf("%02x\n", GenInvSbox(0x00));

    return 0;
}