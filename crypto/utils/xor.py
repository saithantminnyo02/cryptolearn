import base64

def xor_encrypt(text, key):
    if not key:
        return ""
    key_bytes = [ord(k) for k in str(key)]
    result_bytes = bytes([ord(c) ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(text)])
    return base64.b64encode(result_bytes).decode()

def xor_decrypt(cipher_text, key):
    if not key:
        return ""
    key_bytes = [ord(k) for k in str(key)]
    try:
        cipher_bytes = base64.b64decode(cipher_text)
    except Exception:
        return "Invalid base64 input"
    return ''.join(chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(cipher_bytes))