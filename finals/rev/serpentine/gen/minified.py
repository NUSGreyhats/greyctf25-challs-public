def m():
    if __import__("hashlib").sha1(__import__("sys").version.encode()).hexdigest() != "aa7f8dbc4108c4188deae171641908d3ed37e455":
        return
    ct = __import__("ctypes")
    r = __import__("random")
    mm = ct.memmove
    t = ct.cast(id(int) + 96, ct.POINTER(ct.c_uint64)).contents.value
    l = ct.CDLL(None)
    p = t & (~0xfff)
    l.syscall(10, ct.c_uint64(p), 0x1000, 7)
    a = t + 112
    b = t
    c = t + 96
    d = t + 112
    f = b':0oECk`XP6?YMK^t~gu[GW/}wmn\\U>j%$Hr]hiD=eJ9+QI_AN&y58l2pzSO;d{RT(<\'vaLs"-!bxq|Vf37FB*@1Z.#,4)c'
    e = id(f) + 32
    for i in range(33, 127):
        mm(id(i)+24, e, 1)
        e += 1
    global reversed
    def g(l):
        r.seed(69)
        r.shuffle(l)
        mm(c, d, 8)
        mm(a, b, 8)
        l[2] >>= 120
        l[3] >>= 36
        l[8] >>= 83
        l[0] >>= 78
        l[13] >>= 0
        l[7] >>= 61
        l[4] >>= 79
        l[12] >>= 49
        l[6] >>= 87
        l[10] >>= 82
        l[11] >>= 112
        l[1] >>= 99
        l[15] >>= 101
        l[14] >>= 106
        l[9] >>= 49
        l[5] >>= 35
        return l

    reversed = g
m()