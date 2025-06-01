"""
Context:
In a correct proof, for each j such that jacobi(theta_j, N) = 1, the prover
computes sqrt(theta_j) mod p, sqrt(theta_j) mod q, and uses CRT to combine
both into a single mu_j. Note that there are four possible sign choices here,
coming from +-sqrt(theta_j) for both mod p and mod q. Any one of these four
is a valid sqrt(theta_j) mod N.

Attack:
The prover is reusing F, which means that the sequence of challenges theta_1
to theta_m2 are exactly the same because they are deterministic hashes of
N, m_1 + j, and F.

The prover also has a non-deterministic sqrt selection step. This allows an
eavesdropper to get two different valid sqrts for the same theta_j, which
differ by one sign either in mod p or mod q. This means that their difference
will be congruent to 0 in either mod p or q, but not the other.

Therefore, gcd(mu_j_1 - mu_j_2, N) = p or q.
"""

from Crypto.Util.number import GCD, long_to_bytes, inverse

N = 15259097618051614944787283201589661884102249046616617256551480013493757323043057001133186203348289474506700039004930848402024292749905563056243342761253435345816868449755336453407731146923196889610809491263200406510991293039335293922238906575279513387821338778400627499247445875657691237123480841964214842823837627909211018434713132509495011638024236950770898539782783100892213299968842119162995568246332594379413334064200048625302908007017119275389226217690052712216992320294529086400612432370014378344799040883185774674160252898485975444900325929903357977580734114234840431642981854150872126659027766615908376730393
e = 65537
c = 6820410793279074698184582789817653270130724082616000242491680434155953264066785246638433152548701097104342512841159863108848825283569511618965315125022079145973783083887057935295021036668795627456282794393398690975486485865242636068814436388602152569008950258223165626016102975011626088643114257324163026095853419397075140539144105058615243349994512495476754237666344974066561982636000283731809741806084909326748565899503330745696805094211629412690046965596957064965140083265525186046896681441692279075201572766504836062294500730288025016825377342799012299214883484810385513662108351683772695197185326845529252411353

def load_mu_list(path):
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    mu_hexes = lines[1 + 8 : 1 + 8 + 2840]

    mu_list = [int(h, 16) for h in mu_hexes]
    return mu_list, lines[0]

mu_list_1, F1 = load_mu_list("dump1.txt")
mu_list_2, F2 = load_mu_list("dump2.txt")

for j, (m1, m2) in enumerate(zip(mu_list_1, mu_list_2), start=1):
    if m1 != 0 and m2 != 0 and m1 != m2:
        factor = GCD(abs(m1 - m2), N)
        if 1 < factor < N:
            print(f"p = {factor}")
            print(f"q = {N // factor}")
            break

p = factor
q = N // factor

phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(c, d, N)

print(long_to_bytes(m).decode('utf-8', errors='replace'))
