from sage.all import *
from Crypto.Util.number import long_to_bytes
from pwn import *

r = remote("0.cloud.chals.io","28064")
r.sendlineafter("e>","3000000")
a = int(r.recvline().strip().decode())
r.sendlineafter("e>","-2000000") # negative value passes bit_length check
b = int(r.recvline().strip().decode())
r.sendlineafter("e>","5000000")
c = int(r.recvline().strip().decode())
r.sendlineafter("e>","2000001")
d = int(r.recvline().strip().decode())
'''
a ** 2 * b **3
= (m ** 3000000) ** 2 * (m ** -2000000) ** 3
= m ** 6000000 * m ** -6000000
= m ** 0 = 1 (mod n)
'''
e = (a ** 2 * b **3)-1 # Bezout's identity
f = (c ** 2 * b ** 5)-1 # Bezout's identity
g = gcd(e,f) # Their gcb is n

print(g)
c = (d * b) % g # d * b = m ** -2000000 * m ** 2000001 = m ** 1 = m
print(long_to_bytes(c))
