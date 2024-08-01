#! /usr/bin/python3
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
import os
from base64 import b64encode, b64decode

from secret import FLAG

N_PEOPLE = 10
N_BITS = 1024
keys = []
for _ in range(N_PEOPLE):
    p = getPrime(N_BITS//2)
    q = getPrime(N_BITS//2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)

    pubkey = (n, e)
    privkey = d
    keys.append((pubkey, privkey))

flag = bytes_to_long(FLAG + os.urandom(N_BITS//16 - len(FLAG)))

for key, _ in keys:
    n, e = key
    enc = pow(flag, e, n)
    print(b64encode(long_to_bytes(n)).decode())
    print(b64encode(long_to_bytes(e)).decode())
    print(b64encode(long_to_bytes(enc)).decode())

def bit_count(n):
    cnt = 0
    while n:
        cnt += n & 1
        n >>= 1
    return cnt

while True:
    print("1. Send message")
    print("2. Exit")
    inp = int(input().strip())
    if inp == 1:
        inp = int(input("To: ").strip())
        if inp < 0 or inp >= N_PEOPLE:
            print("Invalid")
            exit(0)
        (n, e), d = keys[inp]
        c = bytes_to_long(b64decode(input("Message: ").strip().encode()))
        pt = pow(c, d, n)
        print(bit_count(pt))
    else:
        print("Bye~")
        exit(0)