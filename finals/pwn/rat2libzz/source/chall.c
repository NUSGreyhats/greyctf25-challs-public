// aarch64-linux-gnu-gcc chall.c -L./lib -lzz -no-pie -nostdlib -Wl,-e,_start -o chall

#include <unistd.h>
#include <stdint.h>
#include "libzz.h"

char* freegift = "/bin/sh";

void main(void) {
    volatile uint64_t guard = 0xDEADBEEFCAFEBABEULL;
    char buf[64];
    void (*fp)(int) = &_exit;

    const char prompt[] = "Payload > ";
    write(1, prompt, sizeof(prompt) - 1);
    flusheverything();
    ssize_t n = read(0, buf, 0x100);
    flusheverything();

    if (guard != 0xDEADBEEFCAFEBABEULL) {
        const char warn[] = "Canary corrupted\n";
        write(1, warn, sizeof(warn) - 1);
        flusheverything();
        fp(0);
    } else {
        return 0;
    }
}

__attribute__((naked)) void gift() {
    __asm__ volatile (
        "ldr x1, [sp]\n"
        "ldr x2, [sp,#8]\n"
        "ldr x4, [sp,#16]\n"
        "blr x4"
    );
}

void _start(void)
{
    main();
}


