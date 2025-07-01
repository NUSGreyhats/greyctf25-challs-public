"""
Signing:
k = ???
r = g^k (mod p)
s = (h(m) - x*r) * k^-1 (mod p - 1)

Verifying:
lhs = g^h(m) (mod p)
rhs = y^r * r^s (mod p) = g^(xr) * g^(h(m) - xr) (mod p) = g^h(m) (mod p)

https://core.ac.uk/download/pdf/48535618.pdf

Repeat the solve script until there are no modulus inversion errors
"""

from Crypto.Util.number import *
from pwn import *
import hashlib
import json

context.log_level = 'debug'
# io = process(["python3", "uwusignatures.py"])
io = remote("challs.nusgreyhats.org", 33301)

def hash_m(m):
    sha = hashlib.sha256()
    sha.update(long_to_bytes(m))
    return bytes_to_long(sha.digest())

m = bytes_to_long(b"gib flag pls uwu") # 137457664979133345092444721504268416885
io.recvline()
params = io.recvline()[:-1].decode().split(" ")
p, g, y = int(params[0]), int(params[1]), int(params[2])
# find two distinct m values which produce the same k
io.sendlineafter(b"> ", b"2") 
io.sendlineafter(b"message: ", json.dumps({"m": 1}).encode())
io.recvuntil(b"Here's your uwu signature! ")
params = io.recvline()[:-1].decode()
s1 = int(params)
h1 = hash_m(1)
print(f"s1: {s1}")
print(f"h1: {h1}")

io.sendlineafter(b"> ", b"2") 
io.sendlineafter(b"message: ", json.dumps({"m": 3}).encode())
io.recvuntil(b"Here's your uwu signature! ")
params = io.recvline()[:-1].decode()
s2 = int(params)
h2 = hash_m(3)
print(f"s2: {s2}")
print(f"h2: {h2}")

# s = (h(m) - x*r) * k^-1 (mod p - 1)
if h1 < h2:
    diff = (s2 - s1) % (p - 1)
    kinv = (diff * pow(h2 - h1, -1, p - 1)) % (p - 1)
    k = pow(kinv, -1, p - 1)
    print(f"k comp: {k}")
else:
    diff = (s1 - s2) % (p - 1)
    kinv = (diff * pow(h1 - h2, -1, p - 1)) % (p - 1)
    # print(f"kinv: {res}")
    k = pow(kinv, -1, p - 1)
    print(f"k comp: {k}")

# x = (h1 - s1 * k) * r^-1 (mod (p - 1))
r = pow(g, k, p)
x = ((h1 - s1 * k) * pow(r, -1, p - 1)) % (p - 1)

def sign(m):
    h = hash_m(m)
    r = pow(g, k, p)
    s = ((h - x * r) * pow(k, -1, p - 1)) % (p - 1) 
    return (r, s)

# print(f"signed: {sign(m)}")
final_r, final_s = sign(m)
io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"Send me a message and a signature: ", json.dumps({"m": m, "r": final_r, "s": final_s}).encode())
io.recvline()
io.recvline()
io.interactive()