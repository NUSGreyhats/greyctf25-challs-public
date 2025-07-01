from Crypto.Util.number import *
import json
import hashlib

KEY_LENGTH = 2048
FLAG = "grey{fakeflagfornow}"

class Uwu:
    def __init__(self, keylen):
        self.p = getPrime(keylen)
        self.g = getRandomRange(1, self.p)
        self.x = getRandomRange(2, self.p) # x is private key
        self.y = pow(self.g, self.x, self.p) # y is public key
        self.k = getRandomRange(1, self.p)
        while GCD(self.k, self.p - 1) != 1:
            self.k = getRandomRange(1, self.p)
        print(f"{self.p :} {self.g :} {self.y :}")
        print(f"k: {self.k}")
    def hash_m(self, m):
        sha = hashlib.sha256()
        sha.update(long_to_bytes(m))
        return bytes_to_long(sha.digest())
    def sign(self, m):
        assert m > 0
        assert m < self.p
        h = self.hash_m(m)
        r = pow(self.g, self.k, self.p)
        s = ((h - self.x * r) * pow(self.k, -1, self.p - 1)) % (self.p - 1) 
        return (r, s)
    def verify(self, m, signature):
        r, s = signature
        assert r >= 1
        assert r < self.p
        h = self.hash_m(m)
        lhs = pow(self.g, h, self.p)
        rhs = (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p
        return lhs == rhs 

def main():
    print("Welcome to my super uwu secure digital signature scheme!")
    uwu = Uwu(KEY_LENGTH)
    sign_count = 0   
    while True:
        print("1. Show me some of your cutesy patootie signatures!")
        print("2. Get some of my uwu signatures (max 2)")
        choice = int(input("> "))
        if choice == 1:
            data = json.loads(input("Send me a message and a signature: "))
            m, r, s = data["m"], data["r"], data["s"]
            if m == bytes_to_long(b"gib flag pls uwu"):
                if uwu.verify(m, (r, s)):
                    print("Very cutesy, very mindful, very demure!")
                    print(FLAG)
                    exit()
                else:
                    print("Very cutesy, but not very mindful")
                    exit()
            else:
                print("Not very cutesy")
                exit()
        elif choice == 2:
            if sign_count >= 2:
                print("Y-Y-You'd steal from poor me? U_U")
                exit()
            data = json.loads(input("Send me a message: "))
            m = data["m"]
            if type(m) is not int or m == bytes_to_long(b"gib flag pls uwu"):
                print("Y-Y-You'd trick poor me? U_U")
                exit()
            r, s = uwu.sign(m)
            print(f"Here's your uwu signature! {s :}")
            sign_count += 1
        else:
            print("Not very smart of you OmO")
            exit()

if __name__ == "__main__":
    main()