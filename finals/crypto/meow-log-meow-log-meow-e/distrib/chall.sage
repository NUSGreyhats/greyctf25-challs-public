from Crypto.Util.number import bytes_to_long, getStrongPrime
from random import randint
import json

load("../secret.sage") # e_power

with open("../flag.txt", "rb") as f:
    FLAG = f.read()[:-1]

BITS = 2048
e = 65537
p, q = getStrongPrime(BITS, e), getStrongPrime(BITS, e)
n = p * q
phi = (p - 1) * (q - 1)
d = inverse_mod(e, phi)
assert d > n ^ 0.292, "No Boneh-Durfee for you!"

zr = Zmod(n)

m1 = bytes_to_long(FLAG)

po = randint(65, 128)
# Hint: HUH? WHAT'S E DOING HERE, 
# I THOUGHT THIS WAS A FINITE FIELD????!?!?!?!?!?!?!
m2 = e_power(m1, zr, po)

c1 = zr(m1) ^ e
c2 = zr(m2) ^ e
with open("chall.json", "w") as f:
    json.dump({
        "n": int(n),
        "e": int(e),
        "c1": int(c1),
        "c2": int(c2),
        "po": int(po),
    }, f, indent=4)
print("Challenge generated and saved to chall.json")
