// aarch64-linux-gnu-gcc -nostdlib -fPIC -shared -o libzz.so libzz.c

#include <stdint.h>
#include <sys/types.h>

// Syscall numbers for AArch64 (Linux)
#define SYS_READ   63
#define SYS_WRITE  64
#define SYS_FSYNC  82
#define SYS_EXIT   93

// Raw syscall (3 arguments) for AArch64
static inline long my_syscall3(long num, long arg0, long arg1, long arg2) {
    register long x8  __asm__("x8") = num;
    register long x0  __asm__("x0") = arg0;
    register long x1  __asm__("x1") = arg1;
    register long x2  __asm__("x2") = arg2;

    __asm__ volatile (
        "svc 0"
        : "+r" (x0)
        : "r" (x1), "r" (x2), "r" (x8)
        : "memory"
    );
    return x0;
}

void flusheverything() {
    my_syscall3(SYS_FSYNC, 0, 0, 0);
    my_syscall3(SYS_FSYNC, 1, 0, 0);
    my_syscall3(SYS_FSYNC, 2, 0, 0);
}

// Override read(2)
ssize_t read(int fd, void *buf, size_t count) {
    return my_syscall3(SYS_READ, fd, (long)buf, count);
}

// Override write(2)
ssize_t write(int fd, const void *buf, size_t count) {
    return my_syscall3(SYS_WRITE, fd, (long)buf, count);
}

void _exit(int status) {
    my_syscall3(SYS_EXIT, status, 0, 0);
    while (1) {} // Never returns
}

void one_gadget(void) {
    __asm__ volatile (
        "ldr x8, [sp,#80]\n"
        "ldr x0, [sp,#88]\n"
        "ldr x1, [sp,#96]\n"
        "svc 0"
    );
}

// Stub _init/_fini to suppress loader errors (no libc)
void _init(void) {}
void _fini(void) {}