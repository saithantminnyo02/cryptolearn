import os
from PIL import Image
import numpy as np
from django.core.files.storage import default_storage
from django.conf import settings

def xor_pixels(arr, key):
    key_bytes = [ord(k) for k in key]
    flat = arr.flatten()
    xored = [(p ^ key_bytes[i % len(key_bytes)]) for i, p in enumerate(flat)]
    return np.array(xored, dtype=np.uint8).reshape(arr.shape)

def encrypt_image_file(uploaded_file, key):
    # Save uploaded file manually
    full_path = os.path.join(settings.BASE_DIR, 'media', f'original_{uploaded_file.name}')
    with open(full_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    img = Image.open(full_path)
    arr = np.array(img)

    # XOR encryption
    key_bytes = [ord(k) for k in key]
    flat = arr.flatten()
    xored = [(p ^ key_bytes[i % len(key_bytes)]) for i, p in enumerate(flat)]
    encrypted_arr = np.array(xored, dtype=np.uint8).reshape(arr.shape)

    enc_img = Image.fromarray(encrypted_arr)
    enc_filename = f'enc_{uploaded_file.name}'
    enc_path = os.path.join(settings.BASE_DIR, 'media', enc_filename)
    enc_img.save(enc_path)
    return f'media/{enc_filename}'

def decrypt_image_file(enc_path, key):
    img = Image.open(enc_path)
    arr = np.array(img)
    decrypted_arr = xor_pixels(arr, key)
    dec_img = Image.fromarray(decrypted_arr)
    dec_path = enc_path.replace('enc_', 'dec_')
    dec_img.save(dec_path)
    return dec_path