flag = int.from_bytes(b"grey{h3h3heheh3h3_1_luv_p0lynom1als_s0_much_sie_ist_me1ne_best1e!1!11!!11!!1!!!11!!11!}")

p = random_prime(2^32)
K = GF(p^24,'a')
f = (K.gens()[0].minpoly()).change_ring(ZZ)
R = Zmod(p^24)[x].quo(f)
c = R(x)^flag
K.<a> = Qq(p^24, modulus=f,prec=24)
print(p)
print(f)
print(c)
assert flag == ZZ(sum(ZZ(i)*a^n for n,i in enumerate(c.list())).log()/a.log())
