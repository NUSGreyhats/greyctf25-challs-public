flag = b"nnruMKFLuOAKLuGC"

import random
mapping = b':0oECk`XP6?YMK^t~gu[GW/}wmn\\U>j%$Hr]hiD=eJ9+QI_AN&y58l2pzSO;d{RT(<\'vaLs"-!bxq|Vf37FB*@1Z.#,4)c'
def m(x):
    if type(x) is str:
        x = ord(x)
    if type(x) is bytes:
        x = x[0]
    if x > 127 or x < 33:
        return x
    return mapping[x - 33]
def invm(x):
    if type(x) is int:
        x = bytes([x])
    if type(x) is str:
        x = x.encode()
    if x in mapping:
        return mapping.index(x) + 33
    return x[0]

xor_consts = [78, 99, 120, 36, 79, 35, 87, 61, 83, 49, 82, 112, 49, 0, 106, 101]
flag = [invm(x) for x in flag]
flag = [x ^ m(y) for x,y in zip(flag, xor_consts)]
idx = list(range(16))
random.seed(m(69))
random.shuffle(idx)
flag2 = [flag[idx.index(i)] for i in range(16)]
flag2 = [invm(invm(x) ^ m(42)) for x in flag2]
print(b"grey{"+bytes(flag2)+b"}")