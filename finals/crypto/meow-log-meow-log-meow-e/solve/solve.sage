import json
import sys
from time import time_ns
from Crypto.Util.number import long_to_bytes
load("../secret.sage")

def hgcd(a0, a1, n):
    """
    Half GCD (HGCD) algorithm for polynomials
    
    Sources:
    (1) Algorithm: https://web.archive.org/web/20210512230349/https://web.cs.iastate.edu/~cs577/handouts/polydivide.pdf
    (2) rkm0959's implementation: https://github.com/rkm0959/Implementations/blob/main/Half_GCD/code.sage
    """

    P.<x> = PolynomialRing(Zmod(n))

    # Base case: if deg(a1) ≤ deg(a0)/2, return identity matrix
    if a1.degree() <= a0.degree()/2 or a0.degree() == 1:
        return matrix(P, [[1, 0], [0, 1]])
    
    # Calculate m = floor(deg(a0)/2)
    m = a0.degree() // 2
    
    b0, c0 = a0.quo_rem(x^m)  # b0 = coefficients of x^m and higher terms
    b1, c1 = a1.quo_rem(x^m)  # b1 = coefficients of x^m and higher terms
    
    # Recursive call on quotients
    R = hgcd(b0, b1, n)
    
    # Apply the transformation matrix to [a0, a1]
    d, e = R * vector([a0, a1])
    
    q, r = d.quo_rem(e)
    
    # Calculate floor(m/2) for the next recursion
    xm2 = x ^ (m // 2)
    
    # Split e and f at degree floor(m/2)
    g0, h0 = e.quo_rem(xm2)  # g0 = coefficients of x^[m/2] and higher terms
    g1, h1 = r.quo_rem(xm2)  # g1 = coefficients of x^[m/2] and higher terms
    
    # Recursive call on quotients
    S = hgcd(g0, g1, n)
    
    # Return the combined transformation matrix
    return S * matrix([[0, 1], [1, -q]]) * R


def poly_gcd(a0, a1, n):
    """
    GCD calculation for polynomials using HGCD
    
    Parameters:
    - a0, a1: polynomials in x
    
    Returns:
    - GCD of a0 and a1 (monic)
    """
    # Ensure a0 has higher or equal degree than a1
    if a0.degree() < a1.degree():
        a0, a1 = a1, a0
    
    # Base case: if a1 divides a0, return a1 (made monic)
    if a0 % a1 == 0:
        return a1.monic()
    
    # Recursive case: use HGCD to speed up the calculation
    R = hgcd(a0, a1, n)
    b0, b1 = R * vector([a0, a1])
    
    # Check if b1 divides b0
    if b0 % b1 == 0:
        return b1.monic()
    
    # Continue with standard Euclidean algorithm
    c = b0 % b1
    return poly_gcd(b1, c, n)

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
        gcd = poly_gcd(a0, a1, n)
        gcd = gcd.monic()
        # print(gcd)
        # assert gcd.degree() == 1, "GCD is not linear"
        if gcd.degree() == 1:
            print(f"Found monic linear polynomial at degree {po}: {gcd[0]}")
            m = int(-gcd[0] % n)
            print(f"Message (m): {long_to_bytes(m)}")

    print(f"Time taken: {(time_ns() - start_time) / 1e6:.3f}ms")