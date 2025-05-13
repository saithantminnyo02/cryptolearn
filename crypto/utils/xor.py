def xor_encrypt(text, key):
    key_bytes = [ord(k) for k in key]
    return ''.join(chr(ord(c) ^ key_bytes[i % len(key_bytes)]) for i, c in enumerate(text))

def xor_decrypt(cipher, key):
    return xor_encrypt(cipher, key) 