# Thanks Claude!
def e_power(x, field, terms=20):
    """
    Compute e^x in a finite field using Taylor series approximation.
    
    Args:
        x: element in the finite field
        field: the finite field (e.g., GF(p) or GF(p^n))
        terms: number of Taylor series terms to compute
    
    Returns:
        approximation of e^x in the finite field
    """
    result = field(1)  # Start with e^0 = 1
    x_power = field(1)  # x^0 = 1
    factorial = 1
    
    for n in range(1, terms):
        x_power *= x  # x^n
        factorial *= n  # n!
        
        # In finite fields, we need the multiplicative inverse of factorial
        try:
            factorial_inv = field(factorial)^(-1)
            term = x_power * factorial_inv
            result += term
        except ZeroDivisionError:
            # If factorial is not invertible (divisible by char(field)), skip this term
            continue
    
    return result