from Crypto.Util.number import *
from SECRET import flag

n = 1
for _ in range(4):
    n *= getPrime(1024)

m = bytes_to_long(flag)

try:
    for i in range(4):
        print(f'You have {4-i} change(s).')
        e = int(input(f'Give me your e> '))
        if (e.bit_length() < 20):
            print(f'Your e is too small!')
            exit()
        print(f'{pow(m, e, n)}')
except:
    print(f'Something is error!')
    exit()
