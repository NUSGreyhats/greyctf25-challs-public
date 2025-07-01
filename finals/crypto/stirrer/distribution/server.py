from subprocess import Popen, PIPE
from Crypto.Util.Padding import pad
from os import urandom

KEY = urandom(5)

key_int = int.from_bytes(KEY, byteorder='big')

def encrypt(pt):
	pt = pad(pt, 5)
	cproc = Popen(["./encrypt", str(len(pt)), str(key_int)], stdin=PIPE, stdout=PIPE)
	out, err = cproc.communicate(pt)
	return out
	

def main():
	T = 0
	while T < 1000:
		try:
			pt = input()
			pt = bytes.fromhex(pt)
			if (len(pt) > 10000):
				print("Message too long.")
				exit(1)
				
			ct = encrypt(pt)
			
			if pt == encrypt(KEY): # das crazy
				print(open("flag.txt", "r").read())
				exit(0)
				
			print(ct.hex())
		
		except Exception as e:
			print("Error.")
			exit(1)
		T+=1
	
if __name__ == "__main__":
	main()
