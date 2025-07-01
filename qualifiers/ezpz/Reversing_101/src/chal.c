#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Manual strlen implementation for analysis
int a(char* str) {
	if (!*str) {return 0;}
	char* hm = str;
	while (*++hm);
	return hm - str;
}

uint64_t b() {
    volatile uint64_t a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p;
    volatile uint32_t x1, x2, x3, x4, x5;
    volatile uint8_t t[256];
    register int idx = 0, jdx = 0, kdx = 0;
    
    // Initialize obfuscated lookup table
    for (volatile int z = 0; z < 256; z++) {
        t[z] = (uint8_t)((z * 0x6a) ^ (z >> 1) ^ 0x09 ^ ((z << 3) & 0xe6) ^ (z * z & 0x67));
    }
    
    // Chaotic initialization with stack pollution
    a = 0x9e3779b97f4a7c15ULL; b = a ^ 0x517cc1b727220a95ULL; c = b * 0x85ebca6b0d3e5a45ULL;
    d = c ^ (c >> 17); e = d * a; f = e ^ (e << 13); g = f * b; h = g ^ (g >> 34);
    i = h * c; j = i ^ (i << 26); k = j * d; l = k ^ (k >> 51); m = l * e;
    n = m ^ (m << 39); o = n * f; p = o ^ (o >> 43);
    
    x1 = 0xdeadbeef; x2 = x1 ^ 0x5555aaaa; x3 = x2 * 0xcafe; x4 = x3 ^ 0xbabe; x5 = x4 * 0xfeed;
    
    // Obfuscated computation loops with intentional complexity
    for (volatile int iter = 0; iter < ((a & 0xf) + 7); iter++) {
        idx = (idx + iter * 17 + x1) & 0xff;
        jdx = (jdx + iter * 23 + x2) & 0xff;
        kdx = (kdx + iter * 31 + x3) & 0xff;
        
        // Nested conditional chaos
        if ((iter & 1) ? (a > b) : (c < d)) {
            a = ((a << ((iter % 7) + 1)) | (a >> (64 - ((iter % 7) + 1)))) ^ t[idx];
            b = b * 0x517cc1b727220a95ULL + t[jdx];
            c = c ^ ((c >> ((iter % 13) + 5)) | (c << (64 - ((iter % 13) + 5)))) + t[kdx];
        } else {
            d = d + ((e >> ((iter % 11) + 3)) ^ (f << (64 - ((iter % 11) + 3))));
            e = ((e * 0x9e3779b97f4a7c15ULL) ^ t[(idx + jdx) & 0xff]) + iter;
            f = f ^ ((g << ((iter % 5) + 7)) | (g >> (64 - ((iter % 5) + 7)))) * t[kdx];
        }
        
        // Cross-pollination between variables
        g = (h ^ i) * (j | k) + (l & m) - (n ^ o) + p;
        h = (a + b) ^ (c * d) - (e & f) + (g | h) * t[iter & 0xff];
        i = ((i >> 7) | (i << 57)) ^ ((j << 11) | (j >> 53)) + t[(iter * 7) & 0xff];
        j = j * 0x85ebca6b0d3e5a45ULL ^ ((k >> 13) | (k << 51)) + t[(iter * 11) & 0xff];
        k = k + ((l << 19) | (l >> 45)) ^ ((m >> 23) | (m << 41)) + t[(iter * 13) & 0xff];
        l = l ^ ((n << 29) | (n >> 35)) + ((o >> 31) | (o << 33)) + t[(iter * 17) & 0xff];
        m = m * 0x517cc1b727220a95ULL ^ ((p << 37) | (p >> 27)) + t[(iter * 19) & 0xff];
        n = n + ((a >> 41) | (a << 23)) ^ ((b << 43) | (b >> 21)) + t[(iter * 23) & 0xff];
        o = o ^ ((c << 47) | (c >> 17)) + ((d >> 53) | (d << 11)) + t[(iter * 29) & 0xff];
        p = p * 0x85ebca6b0d3e5a45ULL ^ ((e << 59) | (e >> 5)) + t[(iter * 31) & 0xff];
        
        // Conditional state mixing based on complex predicates
        switch ((iter * x1 + x2 * x3) % 8) {
            case 0: a ^= (b & c) | (d ^ e) + (f * g) - (h & i); break;
            case 1: b += (c | d) ^ (e & f) * (g + h) - (i ^ j); break;
            case 2: c *= ((d ^ e) & (f | g)) + (h * i) ^ (j & k); break;
            case 3: d ^= (e + f) * (g ^ h) & (i | j) + (k & l); break;
            case 4: e += (f * g) ^ (h & i) | (j + k) * (l ^ m); break;
            case 5: f *= (g ^ h) + (i | j) & (k * l) ^ (m + n); break;
            case 6: g ^= (h & i) * (j ^ k) + (l | m) & (n * o); break;
            case 7: h += (i | j) ^ (k * l) & (m + n) * (o ^ p); break;
        }
        
        // More obfuscated mixing with table lookups
        x1 = (x1 << 13) ^ (x1 >> 19) ^ t[(a >> (iter & 7)) & 0xff];
        x2 = (x2 >> 11) ^ (x2 << 21) ^ t[(b >> (iter & 7)) & 0xff];
        x3 = (x3 << 17) ^ (x3 >> 15) ^ t[(c >> (iter & 7)) & 0xff];
        x4 = (x4 >> 23) ^ (x4 << 9) ^ t[(d >> (iter & 7)) & 0xff];
        x5 = (x5 << 7) ^ (x5 >> 25) ^ t[(e >> (iter & 7)) & 0xff];
    }
    
    // Additional obfuscated rounds with different patterns
    for (volatile int round = 0; round < 5; round++) {
        volatile uint64_t temp1 = a, temp2 = b, temp3 = c, temp4 = d;
        
        // Interleaved operations to confuse data flow analysis
        a = ((temp1 * 0x9e3779b97f4a7c15ULL) ^ (temp2 >> 17) ^ (temp3 << 13) ^ (temp4 >> 34)) + t[round * 37 & 0xff];
        b = ((temp2 * 0x85ebca6b0d3e5a45ULL) ^ (temp3 >> 21) ^ (temp4 << 27) ^ (temp1 >> 46)) + t[round * 41 & 0xff];
        c = ((temp3 * 0x517cc1b727220a95ULL) ^ (temp4 >> 29) ^ (temp1 << 35) ^ (temp2 >> 58)) + t[round * 43 & 0xff];
        d = ((temp4 * 0x9e3779b97f4a7c15ULL) ^ (temp1 >> 33) ^ (temp2 << 39) ^ (temp3 >> 62)) + t[round * 47 & 0xff];
        
        // Cross-influence all variables
        e ^= (a & 0x5555555555555555ULL) + (b | 0xaaaaaaaaaaaaaaaaULL);
        f += (c ^ 0x3333333333333333ULL) * (d & 0xccccccccccccccccULL);
        g *= (e | 0x0f0f0f0f0f0f0f0fULL) ^ (f & 0xf0f0f0f0f0f0f0f0ULL);
        h ^= (g + 0x00ff00ff00ff00ffULL) & (a * 0xff00ff00ff00ff00ULL);
        
        // Feedback loops
        i = ((i >> (round * 3 + 7)) | (i << (64 - (round * 3 + 7)))) ^ (j + k + l);
        j = ((j << (round * 5 + 11)) | (j >> (64 - (round * 5 + 11)))) + (m * n * o);
        k = ((k >> (round * 7 + 13)) | (k << (64 - (round * 7 + 13)))) ^ (p + a + b);
        l = ((l << (round * 11 + 17)) | (l >> (64 - (round * 11 + 17)))) + (c * d * e);
        m = ((m >> (round * 13 + 19)) | (m << (64 - (round * 13 + 19)))) ^ (f + g + h);
        n = ((n << (round * 17 + 23)) | (n >> (64 - (round * 17 + 23)))) + (i * j * k);
        o = ((o >> (round * 19 + 29)) | (o << (64 - (round * 19 + 29)))) ^ (l + m + n);
        p = ((p << (round * 23 + 31)) | (p >> (64 - (round * 23 + 31)))) + (o * a * b);
    }
    
    // Final avalanche with maximum confusion
    volatile uint64_t result = a ^ b ^ c ^ d ^ e ^ f ^ g ^ h ^ i ^ j ^ k ^ l ^ m ^ n ^ o ^ p;
    result ^= (result >> 33); result *= 0xff51afd7ed558ccdULL; result ^= (result >> 33);
    result *= 0xc4ceb9fe1a85ec53ULL; result ^= (result >> 33); result += x1 + x2 + x3 + x4 + x5;
    result ^= t[result & 0xff] ^ t[(result >> 8) & 0xff] ^ t[(result >> 16) & 0xff] ^ t[(result >> 24) & 0xff];
    result *= 0x9e3779b97f4a7c15ULL; result ^= (result >> 27); result *= 0x85ebca6b0d3e5a45ULL;
    result ^= (result >> 31); result += 0xdeadbeefcafebabeULL; result ^= (result >> 29);
    
    return result;
}

// RC4 encryption using uint64_t key
void c(uint8_t* data, size_t len, uint64_t key64) {
    uint8_t S[256];
    uint8_t key[8];
    int i, j = 0;
    
    // Convert uint64_t to byte array (little-endian)
    key[0] = (uint8_t)(key64 & 0xFF);
    key[1] = (uint8_t)((key64 >> 8) & 0xFF);
    key[2] = (uint8_t)((key64 >> 16) & 0xFF);
    key[3] = (uint8_t)((key64 >> 24) & 0xFF);
    key[4] = (uint8_t)((key64 >> 32) & 0xFF);
    key[5] = (uint8_t)((key64 >> 40) & 0xFF);
    key[6] = (uint8_t)((key64 >> 48) & 0xFF);
    key[7] = (uint8_t)((key64 >> 56) & 0xFF);
    
    // KSA (Key Scheduling Algorithm)
    for (i = 0; i < 256; i++) {
        S[i] = i;
    }
    
    for (i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % 8]) % 256;
        // Swap S[i] and S[j]
        uint8_t temp = S[i];
        S[i] = S[j];
        S[j] = temp;
    }
    
    // PRGA (Pseudo-Random Generation Algorithm) + Encryption
    i = 0;
    j = 0;
    for (size_t n = 0; n < len; n++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        
        // Swap S[i] and S[j]
        uint8_t temp = S[i];
        S[i] = S[j];
        S[j] = temp;
        
        // Generate keystream byte and XOR with data
        uint8_t K = S[(S[i] + S[j]) % 256];
        data[n] ^= K;
    }
}


void ignore_me_init_buffering() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
}

char enc[] = {0xd1, 0x58, 0x15, 0x8a, 0xee, 0xb5, 0xbb, 0x52, 0x0c, 0x6b, 0xa4, 0xab, 0x6d, 0x7d, 0xb7};
int main() {

	char input[0x100] = {0};

	ignore_me_init_buffering();
	printf("please input the correct password: ");
	scanf("%255s", input);
	input[strcspn(input, "\n")] = '\0';
	if (a(input) == 0xf) {
		c(input, 0xf, b());
		if (!memcmp(input, enc, 0xf)) {
			puts("correct password! answer the quiz to get the flag.");
			return 0;
		}
	}
	puts("incorrect password. try again.");
}

