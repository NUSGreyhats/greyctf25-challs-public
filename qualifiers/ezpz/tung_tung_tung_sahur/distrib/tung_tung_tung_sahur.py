from Crypto.Util.number import getPrime, bytes_to_long

flag = "grey{flag_here}"

e = 3
p, q = getPrime(512), getPrime(512)
N = p * q 
m = bytes_to_long(flag.encode())
C = pow(m,e)

assert C < N 
while (C < N):
    C *= 2
    print("Tung!")

# now C >= N

while (C >= N):
    C -= N 
    print("Sahur!")


print(f"{e = }")
print(f"{N = }")
print(f"{C = }")