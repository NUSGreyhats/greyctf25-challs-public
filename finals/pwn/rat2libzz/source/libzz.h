#ifndef LIBZZ_H
#define LIBZZ_H

#include <sys/types.h>  // for ssize_t

// Low-level syscall interface
long my_syscall3(long num, long arg0, long arg1, long arg2);

// Raw syscall-based I/O overrides
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);

void flusheverything(void);
// Raw syscall-based process exit
void _exit(int status);

// Optional: stubs to suppress loader errors (no-op init/fini)
void _init(void);
void _fini(void);

#endif // LIBZZ_H
