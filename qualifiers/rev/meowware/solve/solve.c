// server.c - Command & Control Server
// Compile with: gcc server.c -o server -lmbedcrypto

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <mbedtls/aes.h>
#include <mbedtls/md.h>

#define SERVER_PORT 443
#define MAX_BUF_SIZE 4096
#define AES_BLOCK_SIZE 16
#define KEY_SIZE 32  // 256-bit key

// Server commands
#define CMD_SHELL "EXIT"
#define CMD_READ "WRITE"
#define CMD_WRITE "READ"
#define CMD_EXIT "SHELL"

// Hard-coded encryption key and IV for the CTF challenge
const unsigned char aes_key[KEY_SIZE+1] = {
	0x4c, 0x75, 0x63, 0x6b, 0x79, 0x20, 0x53, 0x74,
	0x61, 0x72, 0x20, 0x77, 0x61, 0x73, 0x20, 0x68,
	0x65, 0x72, 0x65, 0x2c, 0x20, 0x43, 0x54, 0x46,
	0x20, 0x6b, 0x65, 0x79, 0x20, 0x33, 0x37, 0x21, 0x0
};

const unsigned char aes_iv[AES_BLOCK_SIZE+1] = {
	0x42, 0x61, 0x64, 0x20, 0x52, 0x61, 0x6e, 0x64,
	0x6f, 0x6d, 0x20, 0x49, 0x56, 0x20, 0x3a, 0x29, 0x0
};

unsigned char bytes[] = {0xcd, 0xbb, 0x20, 0xb6, 0x42, 0x74, 0x55, 0x41, 0x4f, 0xe, 0x7f, 0xb, 0x1d, 0xce, 0x71, 0xe7, 0xb, 0xd, 0x62, 0xae, 0x19, 0xba, 0xfa, 0x2b, 0xbb, 0x7a, 0x8f, 0x49, 0xc0, 0x6e, 0x8f, 0xac, 0x90, 0x8b, 0x66, 0x1, 0xaf, 0x41, 0xf1, 0xc, 0x3f, 0x3c, 0x56, 0x5e, 0xd2, 0x1a, 0xda, 0xa5, 0xd5, 0x53, 0xe8, 0x4, 0x8c, 0xf5, 0xd, 0x99, 0xc0, 0x6b, 0xc9, 0xbc, 0xe0, 0xeb, 0xc6, 0xd9};

// Function to remove padding
size_t unpad_data(unsigned char *data, size_t data_len) {
	if (data_len == 0)
		return 0;
		
	unsigned char padding_val = data[data_len - 1];
	
	if (padding_val > AES_BLOCK_SIZE || padding_val == 0)
		return data_len; // Invalid padding, return as is
		
	// Verify padding
	for (size_t i = data_len - padding_val; i < data_len; i++) {
		if (data[i] != padding_val)
			return data_len; // Invalid padding, return as is
	}
	
	return data_len - padding_val;
}
// Function to decrypt data
size_t decrypt_data(unsigned char *ciphertext, size_t ciphertext_len, unsigned char *plaintext) {
	mbedtls_aes_context aes;
	
	// Initialize AES context
	mbedtls_aes_init(&aes);
	mbedtls_aes_setkey_dec(&aes, aes_key, KEY_SIZE * 8);
	
	// Decrypt data block by block
	unsigned char iv[AES_BLOCK_SIZE];
	memcpy(iv, aes_iv, AES_BLOCK_SIZE); // Use a copy of IV
	
	for (size_t i = 0; i < ciphertext_len; i += AES_BLOCK_SIZE) {
		mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_DECRYPT, AES_BLOCK_SIZE,
							 iv, ciphertext + i, plaintext + i);
	}
	
	mbedtls_aes_free(&aes);
	
	// Remove padding
	return unpad_data(plaintext, ciphertext_len);
}

int main() {
	char out[0x80] = {0};
	decrypt_data(bytes, 0x40, out);
	printf("AES Key: %s\n", aes_key);
	printf("AES IV: %s\n", aes_iv);
	printf("Decrypted: %s\n", out);

}
