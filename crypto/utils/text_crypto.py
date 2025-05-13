def generate_key_stream(key: str, length: int) -> list:
    return [ord(key[i % len(key)]) for i in range(length)]

def encrypt_text(text: str, key: str) -> str:
    ks = generate_key_stream(key, len(text))
    return ''.join(chr((ord(c) + k) % 256) for c, k in zip(text, ks))

def decrypt_text(cipher: str, key: str) -> str:
    ks = generate_key_stream(key, len(cipher))
    return ''.join(chr((ord(c) - k) % 256) for c, k in zip(cipher, ks))