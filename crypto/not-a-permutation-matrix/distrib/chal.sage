import random
from base64 import b64encode, b64decode
from functools import reduce

SEED = int(0xcaffe *3* 0xc0ffee)

# https://people.maths.bris.ac.uk/~matyd/GroupNames/61/Q8s5D4.html
G = PermutationGroup([
    [(1,2,3,4),(5,6,7,8),(9,10,11,12),(13,14,15,16),(17,18,19,20),(21,22,23,24),(25,26,27,28),(29,30,31,32)],
    [(1,24,3,22),(2,23,4,21),(5,14,7,16),(6,13,8,15),(9,27,11,25),(10,26,12,28),(17,31,19,29),(18,30,20,32)],
    [(1,5,12,30),(2,6,9,31),(3,7,10,32),(4,8,11,29),(13,25,19,21),(14,26,20,22),(15,27,17,23),(16,28,18,24)],
    [(1,26),(2,27),(3,28),(4,25),(5,14),(6,15),(7,16),(8,13),(9,23),(10,24),(11,21),(12,22),(17,31),(18,32),(19,29),(20,30)]
])
num2e = [*G]
e2num = {y:x for x,y in enumerate(num2e)}
b64encode_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321+/"
b64decode_map = {c:i for i,c in enumerate(b64encode_map)}

def gen_random_mat(seed: int, size: int):
    random.seed(seed)
    return matrix(size, size, random.choices([0,1], k=size*size))

def mat_vec_mul(mat, vec):
    return [reduce(lambda x,y: x*y, (a^b for a,b in zip(vec, m))) for m in mat]

def hash_msg(msg: bytes):
    emsg = b64encode(msg).decode().strip("=")
    sz = len(emsg)
    vec = [num2e[b64decode_map[c]] for c in emsg]
    mat = gen_random_mat(SEED, sz)
    for _ in range(10):
        # Since G is non-abelian, this is a pretty good hash function!
        vec = mat_vec_mul(mat, vec)
    return ''.join((b64encode_map[e2num[c]] for c in vec))

if __name__ == "__main__":
    from flag import flag # secret!!
    import re

    assert re.match(r"^grey\{.+\}$", flag.decode())
    ct = hash_msg(flag)
    print(ct)

# Program output:
# aO3qDbHFoittWTN6MoUYw9CZiC9jdfftFGw1ipES89ugOwk2xCUzDpPdpBWtBP3yarjNOPLXjrMODD
