iv = [True, True, False, True, True, True, None, True, True, False, False, False, None, False, True, True, None, True, True, True, True, False, True, None, False, None, None, None, False, None, False, True, True, True, True, False, False, False, False, False, None, True, True, None, None, False, None, None, False, True, True, False, None, None, None, None, False, False, False, False, False, False, None, None, True, None, True, None, True, False, None, True, False, False, None, None, True, None, True, None, None, True, None, False, None, True, False, True, None, True, None, False, False, False, True, False, False, True, False, False, None, True, False, False, False, True, None, False, True, None, False, None, False, True, True, None, False, True, True, False, None, None, True, True, False, True, None, True, True, True, True, True, False, None, True, None, None, None, None, None, True, None, True, True, True, False, None, False, True, True, True, False, None, True, None, True, True, False, None, None, False, False, False, False, False, None, False, True, None, None, True, True, True, False, False, True, None, None, True, False, True, False, None, True, True, False, False, True, None, True, True, False, None, True, True, True, None, True, True, False, False, True, False, False, None, True, None, False, True, False, False, True, False, False, None, False, True, False, None, None, True, None, True, False, True, None, None, True, None, False, True, True, None, True, False, None, False, False, None]
d = {True:1, False:2, None:0}
iv = [d[x] for x in iv]

N = len(iv)
M = matrix(GF(3), [[0] for i in range(N-1)])
M = M.augment(identity_matrix(N-1))
M = M.stack(matrix([[1 for i in range(N)]]))

R = SL(N, GF(3))
M = R(M)
for i in range(999):
    M = M*M

res= (((M^-1)*(matrix(GF(3), iv).T)).T)
res = [int(x) for x in list(res[0])]
recovered_flag = bytes.fromhex(hex(int("".join(['1' if x == 1 else '0' for x in res]), 2))[2:])
print(recovered_flag)
