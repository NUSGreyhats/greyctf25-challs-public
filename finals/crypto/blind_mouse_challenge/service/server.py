#!/usr/local/bin/python

class Blind:
    def __init__(self):
        self.iv = 0

    def encrypt(self, msg):
        res = ""
        for c in msg:
            res += chr(self._encrypt_single(c))
        return res

    def _encrypt_single(self, char):
        if type(char) != int:
            char = ord(char) - 31
        res = (char ^ self.iv) % 95
        self.iv += 1
        return res + 31

def banner():
    return ("""

       ____()()
      /    ┌─●●
`~~~~~\\_;m__m._>o   blind mouse challenge

""")

def menu():
    return ("""
Menu:
 [F] Encrypt Flag (print encrypted flag)
 [M] Encrypt Message (input your message to encrypt)
 [Q] Quit
 """)

FLAG = "grey{pR3t7y_5urE_c4n_8rUT3_f0rC3}"

def encrypt_flag():
    temp = Blind()
    return temp.encrypt(FLAG)



main = Blind()

if __name__ == "__main__":
    print(banner())
    while (1):
        print(menu())
        choice = input("> ").upper()[0]
        print()
        if (choice == 'F'):
            print("Encrypted flag:",encrypt_flag())
        elif (choice == 'M'):
            print("\nEncrypted msg :", main.encrypt(input("Message to encrypt:\n> ")))
        elif (choice == 'Q'):
            exit(0)