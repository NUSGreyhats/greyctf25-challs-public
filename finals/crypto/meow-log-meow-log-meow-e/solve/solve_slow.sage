import sys
import json
from Crypto.Util.number import long_to_bytes
from time import time_ns

load("../secret.sage")  # Load the e_power function

def naive_gcd(a, b):
    """
    Compute the GCD of two polynomials using the naive method
    """
    while b != 0:
        a, b = b, a % b
        # print(a, b)
    return a

if __name__ == "__main__":
    sys.setrecursionlimit(10 ** 6)

    # Start the timer
    start_time = time_ns()
    # Now break the challenge
    with open("../distrib/chall.json", "r") as f:
        data = json.load(f)
        n = data["n"]
        e = data["e"]
        c1 = data["c1"]
        c2 = data["c2"]
        po = data["po"]
        # Convert to polynomial ring
        F = Zmod(n)
        R.<x> = PolynomialRing(F)

        # Create polynomials from the ciphertexts
        a0 = x^e - c1
        a1 = e_power(x, F, po)^e - c2
        # Compute the GCD
        gcd = naive_gcd(a0, a1)
        gcd = gcd.monic()
        # print(gcd)
        # assert gcd.degree() == 1, "GCD is not linear"
        if gcd.degree() == 1:
            print(f"Found monic linear polynomial at degree {po}: {gcd[0]}")
            m = int(-gcd[0] % n)
            print(f"Message (m): {long_to_bytes(m)}")

    print(f"Time taken: {(time_ns() - start_time) / 1e6:.3f}ms")