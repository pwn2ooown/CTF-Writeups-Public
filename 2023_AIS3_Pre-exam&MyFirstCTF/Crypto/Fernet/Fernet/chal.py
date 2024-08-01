import os
import base64
from cryptography.fernet import Fernet
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from secret import FLAG

def encrypt(plaintext, password):
    salt = os.urandom(16)  
    key = PBKDF2(password.encode(), salt, 32, count=1000, hmac_hash_module=SHA256)  
    f = Fernet(base64.urlsafe_b64encode(key))  
    ciphertext = f.encrypt(plaintext.encode())  
    return base64.b64encode(salt + ciphertext).decode()

# Usage:
leak_password = 'mysecretpassword'
plaintext = FLAG

# Encrypt
ciphertext = encrypt(plaintext, leak_password)
print("Encrypted data:",ciphertext)


