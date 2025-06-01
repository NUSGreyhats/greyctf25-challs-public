import hashlib
from math import ceil, log2
from pwn import remote
from Crypto.Util.number import GCD, inverse
import random

# Secret values for p and q
p = 1337
q = 1337

N = (
    15259097618051614944787283201589661884102249046616617256551480013493757323043057001133186203348289474506700039004930848402024292749905563056243342761253435345816868449755336453407731146923196889610809491263200406510991293039335293922238906575279513387821338778400627499247445875657691237123480841964214842823837627909211018434713132509495011638024236950770898539782783100892213299968842119162995568246332594379413334064200048625302908007017119275389226217690052712216992320294529086400612432370014378344799040883185774674160252898485975444900325929903357977580734114234840431642981854150872126659027766615908376730393
)

# From https://rosettacode.org/wiki/Jacobi_symbol#Python
def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        e = 0
        while a % 2 == 0:
            a //= 2
            e += 1
        if e % 2 == 1:
            if n % 8 in (3, 5):
                result = -result
        if (a % 4 == 3) and (n % 4 == 3):
            result = -result
        a, n = n % a, a
    if n == 1:
        return result
    else:
        return 0

# From https://rosettacode.org/wiki/Tonelli-Shanks_algorithm#Python
def legendre(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli(n, p):
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def crt_combine(r_p, p, r_q, q):
    inv_p_mod_q = inverse(p, q)
    y = ((r_q - r_p) * inv_p_mod_q) % q
    x = r_p + p * y
    return x % (p * q)

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8 or 1, 'big')

def gen_rho_ZN(N, idx):
    attempt = 0
    while True:
        h = hashlib.sha256()
        h.update(b'Z')
        h.update(int_to_bytes(N))
        h.update(idx.to_bytes(4, 'big'))
        h.update(attempt.to_bytes(4, 'big'))
        candidate = int.from_bytes(h.digest(), 'big') % N
        if 1 < candidate < N and GCD(candidate, N) == 1:
            return candidate
        attempt += 1

def gen_theta_J(N, idx, F_bytes):
    attempt = 0
    while True:
        h = hashlib.sha256()
        h.update(b'J')
        h.update(int_to_bytes(N))
        h.update(idx.to_bytes(4, 'big'))
        h.update(F_bytes)
        h.update(attempt.to_bytes(4, 'big'))
        candidate = int.from_bytes(h.digest(), 'big') % N
        if 1 < candidate < N and GCD(candidate, N) == 1 and jacobi(candidate, N) == 1:
            return candidate
        attempt += 1

kappa = 128
alpha = 65537
m1 = ceil(kappa / log2(alpha))
m2 = ceil(kappa * 32 * 0.69314718056)

phi = (p - 1) * (q - 1)

F_bytes = b'this_is_a_secret'
F_hex = F_bytes.hex()

sigmas = []
invN_mod_phi = inverse(N, phi)
for i in range(1, m1 + 1):
    rho_i = gen_rho_ZN(N, i)
    sigma_i = pow(rho_i, invN_mod_phi, N)
    sigmas.append(sigma_i)

flip_prob = 0.5
mus = []
for j in range(1, m2 + 1):
    theta_j = gen_theta_J(N, m1 + j, F_bytes)

    if pow(theta_j, (p - 1) // 2, p) == 1 and pow(theta_j, (q - 1) // 2, q) == 1:
        r_p = tonelli(theta_j % p, p)
        r_q = tonelli(theta_j % q, q)
        if random.random() < flip_prob:
            r_p = -r_p % p
        mu_j = crt_combine(r_p, p, r_q, q)
        mus.append(mu_j)
    else:
        mus.append(0)


HOST = "127.0.0.1"
PORT = 1337
conn = remote(HOST, PORT)

# Makeshift wireshark
# I hate parsing pcaps as much as the next guy
with open(f"dump.txt", "w") as dump_f:
    dump_f.write(F_hex + "\n")
    conn.sendline(F_hex)

    for sigma in sigmas:
        line = format(sigma, "x")
        dump_f.write(line + "\n")
        conn.sendline(format(sigma, "x"))

    for mu in mus:
        line = format(mu, "x")
        dump_f.write(line + "\n")
        conn.sendline(format(mu, "x"))

    try:
        reply = conn.recvline(timeout=5)
        if reply:
            dump_f.write(reply.decode().strip() + "\n")
            print("Verifier response:", reply.decode().strip())
    except:
        pass

conn.close()
