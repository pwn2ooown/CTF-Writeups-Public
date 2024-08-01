import os
import base64
from cryptography.fernet import Fernet
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

# from secret import FLAG


def encrypt(plaintext, password):
    salt = os.urandom(16)
    key = PBKDF2(password.encode(), salt, 32, count=1000, hmac_hash_module=SHA256)
    f = Fernet(base64.urlsafe_b64encode(key))
    ciphertext = f.encrypt(plaintext.encode())
    return base64.b64encode(salt + ciphertext).decode()


# Usage:
leak_password = "mysecretpassword"
plaintext = "FLAG"

# Encrypt
ciphertext = encrypt(plaintext, leak_password)
print("Encrypted data:", ciphertext)
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives import padding


def decrypt(ciphertext, password):
    decoded = base64.b64decode(ciphertext)
    salt = decoded[:16]
    ciphertext = decoded[16:]
    key = PBKDF2(password.encode(), salt, 32, count=1000, hmac_hash_module=SHA256)
    f = Fernet(base64.urlsafe_b64encode(key))
    plaintext = f.decrypt(ciphertext)
    return plaintext.decode()


print(
    decrypt(
        "iAkZMT9sfXIjD3yIpw0ldGdBQUFBQUJrVzAwb0pUTUdFbzJYeU0tTGQ4OUUzQXZhaU9HMmlOaC1PcnFqRUIzX0xtZXg0MTh1TXFNYjBLXzVBOVA3a0FaenZqOU1sNGhBcHR3Z21RTTdmN1dQUkcxZ1JaOGZLQ0E0WmVMSjZQTXN3Z252VWRtdXlaVW1fZ0pzV0xsaUM5VjR1ZHdj",
        leak_password,
    )
)
