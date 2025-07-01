def safeXor(a,b): # in case of none input
    if a is None: return b
    if b is None: return a
    if a==b: return not a
    return None

from functools import reduce
flag = b"grey{!safe,_!xor,_wow..,..,.,}"
iv = [True if int(i) else False for i in bin(int(flag.hex(),16)).lstrip("0b")]
for _ in range(1<<20):
    iv = iv[1:] + [reduce(safeXor,iv)]
    
print(iv[:50])