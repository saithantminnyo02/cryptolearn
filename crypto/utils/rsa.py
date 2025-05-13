from math import gcd

def modinv(a, m):
    """Modular inverse using Extended Euclidean Algorithm"""
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime with (p-1)*(q-1)")
    d = modinv(e, phi)
    return (e, n), (d, n)

def rsa_encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(cipher, d, n):
    return ''.join([chr(pow(c, d, n)) for c in cipher])