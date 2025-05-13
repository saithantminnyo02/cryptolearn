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
    form = RSAForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get("action")
        if form.is_valid():
            message = form.cleaned_data['message']
            p = form.cleaned_data['p']
            q = form.cleaned_data['q']
            e = form.cleaned_data['e']
            try:
                public_key, private_key = rsa.generate_keys(p, q, e)
                if action == 'encrypt':
                    encrypted = rsa.rsa_encrypt(message, *public_key)
                elif action == 'decrypt':
                    # Expect comma-separated numbers as input for ciphertext
                    ciphertext = list(map(int, message.split(',')))
                    decrypted = rsa.rsa_decrypt(ciphertext, *private_key)
            except Exception as ex:
                form.add_error(None, str(ex))

    return render(request, 'rsa_combined.html', {
        'form': form,
        'encrypted': encrypted,
        'decrypted': decrypted,
        'public_key': public_key,
        'private_key': private_key,
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
            try:
                if algo == 'caesar':
                    shift = int(key)
                    if action == 'encrypt':
                        result = caesar.caesar_encrypt(text, shift)
                        decrypted = caesar.caesar_decrypt(result, shift)
                    elif action == 'decrypt':
                        decrypted = caesar.caesar_decrypt(text, shift)

                elif algo == 'xor':
                    if action == 'encrypt':
                        result = xor.xor_encrypt(text, key)
                        decrypted = xor.xor_decrypt(result, key)
                    elif action == 'decrypt':
                        decrypted = xor.xor_decrypt(text, key)

                elif algo == 'rail':
                    rails = int(key)
                    if rails < 2:
                        form.add_error('key', 'Number of rails must be at least 2.')
                    else:
                        if action == 'encrypt':
                            result = railfence.rail_fence_encrypt(text, rails)
                            decrypted = railfence.rail_fence_decrypt(result, rails)
                        elif action == 'decrypt':
                            decrypted = railfence.rail_fence_decrypt(text, rails)
            except Exception as ex:
                form.add_error(None, f"Error: {str(ex)}")

    return render(request, 'text_cipher_combined.html', {
        'form': form,
        'algo': algo,
        'encrypted': result if request.POST.get("action") == 'encrypt' else None,
        'decrypted': decrypted if request.POST.get("action") == 'decrypt' else None,
    })

def home(request):
    return render(request, 'home.html')