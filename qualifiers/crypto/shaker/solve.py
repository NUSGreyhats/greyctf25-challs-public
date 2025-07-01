from pwn import *
import hashlib 
context.log_level = 'error'
for _ in range(1000):
    r = remote("127.0.0.1", 32222)

    r.sendline(b"2")
    r.readuntil(b"Result: ")
    T = 120
    for i in range(T-1):
        r.sendline(b"1")

    r.sendline(b"2")
    r.readuntil(b"Result: ")
    R = r.readline().decode()
    R = bytes.fromhex(R)
    if hashlib.md5(R).hexdigest() == "4839d730994228d53f64f0dca6488f8d":
        print(_, R)
        break
    r.close()
