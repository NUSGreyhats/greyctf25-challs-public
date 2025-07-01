from pwn import *
from subprocess import Popen, PIPE
import time
import random
from Crypto.Util.Padding import pad

r = remote("127.0.0.1", 5000)


def rotl8(x, n):
    return ((x << n) | (x >> (8 - n))) & 0xff

d = {}

pairs = []

PT = b""
CT = b""


def encrypt(pt, key):
	
	key_int = int.from_bytes(key, byteorder='big')
	pt = pad(pt, 5)
	cproc = Popen(["./encrypt", str(len(pt)), str(key_int)], stdin=PIPE, stdout=PIPE)
	out, err = cproc.communicate(pt)
	return out

T = time.time()
cnt = 0
for i in range(999):
	K = random.randbytes(5000)
	r.sendline(K.hex().encode())
	res = bytes.fromhex(r.readline().decode())
	PT += K[:5000]
	CT += res[:5000]
		
print(time.time()-T)

cproc = Popen("./solve", stdin=PIPE, stdout=PIPE)
out, err = cproc.communicate(PT + CT)

for line in out.decode().splitlines():
	
	test_key = bytes(map(int, line.split()))
	test_pt = PT[:5]
	test_ct = CT[:5]
	res_ct = encrypt(test_pt, test_key)[:5]
	if (res_ct == test_ct):
		enc_key = encrypt(test_key, test_key)
		
		r.sendline(enc_key.hex().encode())
		ret = r.readline().decode()
		print(ret)
		break
		
print(time.time() - T)

