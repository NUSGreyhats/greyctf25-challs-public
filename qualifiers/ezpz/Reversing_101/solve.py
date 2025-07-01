from pwn import *

p = remote("localhost", 33000)

p.sendlineafter(b"Answer:", b"0x402db6")
p.sendlineafter(b"Answer:", b"strlen")
p.sendlineafter(b"Answer:", b"0xf")
p.sendlineafter(b"Answer:", b"0xc1de1494171d9e2f")
p.sendlineafter(b"Answer:", b"rc4")
p.sendlineafter(b"Answer:", b"honk-mimimimimi")

p.interactive()
