key = [0x73, 0x44, 0x64, 0x61]
text = "badddd"
cry = [ord(c) for c in "googoogaga"]

def mul(a, b):
    res = [0] * 2
    res[0] = (a[0] * b[0] + a[1] * b[1]) % 256
    res[1] = (a[2] * b[0] + a[3] * b[1]) % 256
    return res

output = []
with open("catt.enc", "rb") as f:
    output = [x for x in f.read()]

for i in range(len(output)):
    output[i] ^= cry[i % len(cry)]



det = (0x73 * 0x61) - (0x44 * 0x64)

adjoint = [0x61, -0x44, -0x64, 0x73]
mod_inv = 0
while (mod_inv * det) % 256 != 1:
    mod_inv += 1
print(det)
print(mod_inv)
inverse = [(mod_inv * x) % 256 for x in adjoint]
decrypt = [0] * len(output)
i = 0
while i * 2 != len(output):
    die = output[i * 2:((i+1)*2)]
    res = mul(inverse,die)
    decrypt[i*2] = res[0]
    decrypt[i*2+1] = res[1]
    i += 1

bruh = [int(x) for x in decrypt]
with open("testt.jpg", "wb") as f: 
    f.write(bytes(bruh))



