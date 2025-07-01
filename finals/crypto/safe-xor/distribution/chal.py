def safeXor(a,b): # in case of none input
    if a is None: return b
    if b is None: return a
    if a==b: return not a
    return None

from functools import reduce
flag = b"grey{?????????????????????}"
iv = [True if int(i) else False for i in bin(int(flag.hex(),16)).lstrip("0b")]
for _ in range(2**999):
    iv = iv[1:] + [reduce(safeXor,iv)]
assert iv == [True, True, False, True, True, True, None, True, True, False, False, False, None, False, True, True, None, True, True, True, True, False, True, None, False, None, None, None, False, None, False, True, True, True, True, False, False, False, False, False, None, True, True, None, None, False, None, None, False, True, True, False, None, None, None, None, False, False, False, False, False, False, None, None, True, None, True, None, True, False, None, True, False, False, None, None, True, None, True, None, None, True, None, False, None, True, False, True, None, True, None, False, False, False, True, False, False, True, False, False, None, True, False, False, False, True, None, False, True, None, False, None, False, True, True, None, False, True, True, False, None, None, True, True, False, True, None, True, True, True, True, True, False, None, True, None, None, None, None, None, True, None, True, True, True, False, None, False, True, True, True, False, None, True, None, True, True, False, None, None, False, False, False, False, False, None, False, True, None, None, True, True, True, False, False, True, None, None, True, False, True, False, None, True, True, False, False, True, None, True, True, False, None, True, True, True, None, True, True, False, False, True, False, False, None, True, None, False, True, False, False, True, False, False, None, False, True, False, None, None, True, None, True, False, True, None, None, True, None, False, True, True, None, True, False, None, False, False, None]
