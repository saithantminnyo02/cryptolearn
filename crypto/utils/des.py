from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def des_encrypt(plaintext: str, key: str) -> str:
    k = key.encode('utf-8')[:8].ljust(8, b'_')  # DES requires 8-byte key
    iv = get_random_bytes(8)  # IV is also 8 bytes for DES
    cipher = DES.new(k, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), 8))
    encrypted_data = iv + ciphertext  # prepend IV for later decryption
    return base64.b64encode(encrypted_data).decode('utf-8')

def des_decrypt(cipher_b64: str, key: str) -> str:
    k = key.encode('utf-8')[:8].ljust(8, b'_')
    raw = base64.b64decode(cipher_b64)
    iv = raw[:8]
    ciphertext = raw[8:]
    cipher = DES.new(k, DES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 8)
    return plaintext.decode('utf-8')