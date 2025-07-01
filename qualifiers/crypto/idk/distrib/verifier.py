import hashlib
from math import ceil, log2
from pwn import listen
from Crypto.Util.number import GCD

N = 15259097618051614944787283201589661884102249046616617256551480013493757323043057001133186203348289474506700039004930848402024292749905563056243342761253435345816868449755336453407731146923196889610809491263200406510991293039335293922238906575279513387821338778400627499247445875657691237123480841964214842823837627909211018434713132509495011638024236950770898539782783100892213299968842119162995568246332594379413334064200048625302908007017119275389226217690052712216992320294529086400612432370014378344799040883185774674160252898485975444900325929903357977580734114234840431642981854150872126659027766615908376730393

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
threshold = (3 * m2) // 8 

server = listen(1337)
conn = server.wait_for_connection()

line = conn.recvline(timeout=30)
if not line:
    conn.sendline(b"FAIL")
    conn.close()
    exit(1)
try:
    F_bytes = bytes.fromhex(line.decode().strip())
except:
    conn.sendline(b"FAIL")
    conn.close()
    exit(1)

sigmas = []
for _ in range(m1):
    line = conn.recvline(timeout=30)
    if not line:
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)
    try:
        sigmas.append(int(line.decode().strip(), 16))
    except:
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)

mus = []
for _ in range(m2):
    line = conn.recvline(timeout=30)
    if not line:
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)
    try:
        mus.append(int(line.decode().strip(), 16))
    except:
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)

for i in range(1, m1 + 1):
    sigma_i = sigmas[i - 1]
    if not (0 < sigma_i < N):
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)
    rho_i = gen_rho_ZN(N, i)
    if pow(sigma_i, N, N) != rho_i:
        conn.sendline(b"FAIL")
        conn.close()
        exit(1)

count_nonzero = 0
for j in range(1, m2 + 1):
    mu_j = mus[j - 1]
    theta_j = gen_theta_J(N, m1 + j, F_bytes)
    if mu_j != 0:
        count_nonzero += 1
        if not (0 < mu_j < N):
            conn.sendline(b"FAIL")
            conn.close()
            exit(1)
        if pow(mu_j, 2, N) != theta_j:
            conn.sendline(b"FAIL")
            conn.close()
            exit(1)

if count_nonzero < threshold:
    conn.sendline(b"FAIL")
    conn.close()
    exit(1)

conn.sendline(b"OK")
conn.close()
