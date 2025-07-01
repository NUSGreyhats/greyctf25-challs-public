fake = b"im_fake_flag_XDD"
fake = bytes(reversed([x ^ 42 for x in fake]))
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


xor = lambda x,y: bytes(a^b for a,b in zip(x,y))

target = b"m3553d_up_py7h0n"
target = [m(m(x) ^ m(42)) for x in target]
random.seed(m(69))
random.shuffle(target)
for i, x in enumerate(xor([invm(y) for y in fake], target)):
    print(f"l[{i}] >>= {invm(x)}")