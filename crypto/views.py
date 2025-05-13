from django.shortcuts import render
from .forms import DESForm, TextEncryptForm
from .utils.image_crypto import encrypt_image_file, decrypt_image_file
import base64
from .utils import caesar, xor, railfence, des




from .forms import RSAForm
from .utils import rsa
    
def des_combined_view(request):
    encrypted = None
    decrypted = None
    error = None
    form = DESForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get("action")
        if form.is_valid():
            text = form.cleaned_data['text']
            key = form.cleaned_data['key']
            if len(key.encode('utf-8')) != 8:
                form.add_error('key', 'DES key must be exactly 8 bytes.')
            else:
                try:
                    if action == 'encrypt':
                        encrypted = des.des_encrypt(text, key)
                        decrypted = des.des_decrypt(encrypted, key)
                    elif action == 'decrypt':
                        decrypted = des.des_decrypt(text, key)
                except Exception as ex:
                    error = f"Decryption failed: {str(ex)}"

    return render(request, 'des_combined.html', {
        'form': form,
        'encrypted': encrypted,
        'decrypted': decrypted if request.POST.get("action") == 'decrypt' else None,
        'error': error,
    })

def rsa_combined_view(request):
    encrypted = None
    decrypted = None
    public_key = None
    private_key = None
    decrypted_ints = None
    encrypted_ints = None
    form = RSAForm(request.POST or None)
    action = request.POST.get("action", "") if request.method == "POST" else ""  
    encrypted_number = None
    encrypted_char = None

    # These must exist in rsa.py
    # def rsa_encrypt_single(m, e, n): return pow(m, e, n)
    # def rsa_decrypt_single(c, d, n): return pow(c, d, n)

    if request.method == 'POST':
        if form.is_valid():
            message = form.cleaned_data['message']
            p = form.cleaned_data['p']
            q = form.cleaned_data['q']
            e = form.cleaned_data['e']
            try:
                phi_n = (p - 1) * (q - 1)
                if not (1 < e < phi_n):
                    raise ValueError(f"Public exponent e must satisfy 1 < e < φ(n) = {phi_n}")
                public_key, private_key = rsa.generate_keys(p, q, e)
                if action == 'encrypt':
                    try:
                        msg_int = int(message)
                        encrypted_single = rsa.rsa_encrypt_single(msg_int, *public_key)
                        encrypted_number = encrypted_single
                        encrypted_char = chr(encrypted_single) if 0 <= encrypted_single <= 1114111 else ''
                    except ValueError:
                        form.add_error('message', 'Input must be a number for integer encryption.')
                elif action == 'decrypt':
                    try:
                        if ',' in message:
                            ciphertext = list(map(int, message.split(',')))
                            decrypted_ints = rsa.rsa_decrypt(ciphertext, *private_key)
                            decrypted = ''.join(chr(i) for i in decrypted_ints)
                        else:
                            decrypted_int = rsa.rsa_decrypt_single(int(message), *private_key)
                            decrypted = str(decrypted_int)
                            decrypted_ints = [decrypted_int]
                    except ValueError:
                        form.add_error('message', 'Invalid encrypted input format.')
            except Exception as ex:
                form.add_error(None, str(ex))

    return render(request, 'rsa_combined.html', {
        'form': form,
        'decrypted': decrypted,
        'public_key': public_key,
        'private_key': private_key,
        'encrypted_number': encrypted_number if action == 'encrypt' else None,
        'encrypted_char': encrypted_char if action == 'encrypt' else None,
    })

def text_cipher_combined_view(request):
    result = None
    decrypted = None
    algo = None
    form = TextEncryptForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get("action")
        if form.is_valid():
            algo = form.cleaned_data['algorithm']
            text = form.cleaned_data['text']
            key = form.cleaned_data['key']
            # Algorithm logic block (corrected version)
            if algo == 'caesar':
                try:
                    shift = int(key)
                    if action == 'encrypt':
                        result = caesar.caesar_encrypt(text, shift)
                        decrypted = caesar.caesar_decrypt(result, shift)
                    elif action == 'decrypt':
                        decrypted = caesar.caesar_decrypt(text, shift)
                except ValueError:
                    form.add_error('key', 'Key must be an integer for Caesar Cipher.')

            elif algo == 'xor':
                try:
                    if not key or len(key) != 1:
                        form.add_error('key', 'Key must be exactly 1 character for XOR Cipher.')
                        raise ValueError('Invalid XOR key.')

                    key_char = key[0]
                    if action == 'encrypt':
                        result = ''.join(chr(ord(c) ^ ord(key_char)) for c in text)
                        decrypted = ''.join(chr(ord(c) ^ ord(key_char)) for c in result)
                    elif action == 'decrypt':
                        decrypted = ''.join(chr(ord(c) ^ ord(key_char)) for c in text)
                except Exception as e:
                    form.add_error(None, f"XOR Cipher Error: {str(e)}")

            elif algo == 'rail':
                try:
                    rails = int(key)
                    if rails < 2:
                        form.add_error('key', 'Number of rails must be at least 2.')
                    else:
                        if action == 'encrypt':
                            result = railfence.rail_fence_encrypt(text, rails)
                            decrypted = railfence.rail_fence_decrypt(result, rails)
                        elif action == 'decrypt':
                            decrypted = railfence.rail_fence_decrypt(text, rails)
                except ValueError:
                    form.add_error('key', 'Key must be a number for Rail Fence Cipher.')

    return render(request, 'text_cipher_combined.html', {
        'form': form,
        'algo': algo,
        'encrypted': result if request.POST.get("action") == 'encrypt' else None,
        'decrypted': decrypted if request.POST.get("action") == 'decrypt' else None,
    })

def home(request):
    return render(request, 'home.html')