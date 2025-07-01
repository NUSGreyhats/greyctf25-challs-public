flag = b"grey{!safe,_!xor,_wow..,..,.,}"
iv = [1 if int(i) else -1 for i in bin(int(flag.hex(),16)).lstrip("0b")]
N = len(iv)
M = matrix(GF(3), [[0] for i in range(N-1)])
M = M.augment(identity_matrix(N-1))
M = M.stack(matrix([[1 for i in range(N)]]))

R = SL(N, GF(3))
M = R(M)
for i in range(999):
    M = M*M
print((M*(matrix(GF(3), iv).T)).T)