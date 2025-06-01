// gcc -no-pie -g baby_bytes.c -o baby_bytes

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/mman.h>

void setup(){
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

void printmenu() {
    printf("Choose an option:\n");
    printf("1. Read any byte\n");
    printf("2. Write any byte\n");
    printf("> ");
}

void win() {
    execve("/bin/sh", 0, 0);
}

int main() {
    setup();
    puts("Welcome to the extremely vulnerable baby bytes game!");
    puts("Where we allow you to read and write any byte you want, no strings attached!");
    int choice = 0;
    printf("Here's your address of choice (pun intended): %p\n", &choice);
    printf("You need to call the function at this address to win: %p\n", win);
    while (true) {
        printmenu();
        scanf("%d", &choice);
        if (choice == 1) {
            puts("Enter the address of the byte you want to read in hex:");
            char* ptr = NULL;
            scanf("%llx", &ptr);
            printf("Your byte is: %02hhx\n", *ptr);
        } else if (choice == 2) {
            puts("Enter the address of the byte you want to write to in hex:");
            char* ptr = NULL;
            scanf("%llx", &ptr);
            puts("Enter the byte you want to change it to:");
            char changeto;
            scanf("%hhx", &changeto);
            mprotect(ptr, 1, PROT_READ | PROT_WRITE | PROT_EXEC);
            *ptr = changeto;
        } else {
            puts("Invalid option! Exiting...");
            break;
        }
    }
}