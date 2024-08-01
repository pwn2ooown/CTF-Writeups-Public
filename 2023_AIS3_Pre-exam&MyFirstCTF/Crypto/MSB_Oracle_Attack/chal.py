import os
import random
from Crypto.Util.number import getPrime


p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))

print(f'Your key: {hex(n)} {hex(e)}')

secret = random.randrange(n)
hint = pow(secret, e, n)

print(f'Your hint: {hex(hint)}')

for _ in range(1500):
    ct = int(input('The ciphertext? '), 16)
    if ct == 0:
        break
    pt = pow(ct, d, n)
    if pt > n // 2:
        print('Your plaintext is big')
    else:
        print('Your plaintext is small')

if input('The secret? ') == hex(secret):
    flag = os.environ['FLAG']
    print(f'Your flag: {flag}')
else:
    print('No flag')
