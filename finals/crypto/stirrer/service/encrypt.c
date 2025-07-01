#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

#define N 5

uint8_t key[N];

// 8-bit left rotation
inline uint8_t rotl8(uint8_t x, int n) {
    return (uint8_t)((x << n) | (x >> (8 - n)));
}


inline void block(uint8_t* state) {
    
    for (int i = 0; i < N; i++)
        state[i] = (state[i] + key[i]) & 0xFF;
    
    state[0] = (state[0] + state[1]) & 0xFF;
    state[3] ^= state[0];
    state[3] = rotl8(state[3], 1);

    state[2] = (state[2] + state[4]) & 0xFF;
    state[0] ^= state[2];
    state[0] = rotl8(state[0], 7);

    state[1] = (state[1] + state[2]) & 0xFF;
    state[4] ^= state[1];
    state[4] = rotl8(state[4], 2);
    
    for (int i = 0; i < N; i++)
        state[i] = (state[i] + key[i]) & 0xFF;

}


void encrypt(uint8_t *pt, uint8_t *ct, size_t len) {
    memcpy(ct, pt, len);
    for (size_t i = 0; i < len; i+=5) {

        for (int t = 0; t < 1000; t++)
            block(ct + i);

    }
}

int main(int argc, char** argv) {
    
    
    int LEN = atoi(argv[1]);
    long KEY = atol(argv[2]);
    
    key[0] = (KEY >> 32) & 0xff;
    key[1] = (KEY >> 24) & 0xff;
    key[2] = (KEY >> 16) & 0xff;
    key[3] = (KEY >> 8) & 0xff;
    key[4] = KEY & 0xff;
    
    
    uint8_t *pt = malloc(LEN);
    uint8_t *ct = malloc(LEN);
    if (!pt || !ct) return 1;

    fread(pt, sizeof *pt, LEN, stdin);

    encrypt(pt, ct, LEN);

    fwrite(ct, sizeof *ct, LEN, stdout);
    
    free(pt);
    
    free(ct);
    return 0;
}

