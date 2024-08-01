#! /usr/bin/python3
from Crypto.Util.number import getStrongPrime, bytes_to_long
import os
import random
import math
from secret import FLAG

p1 = getStrongPrime(1024)
q1 = getStrongPrime(1024)
n = p1 * q1
p2 = getStrongPrime(2048)

while True:
    g1 = random.randint(1, p1 * q1)
    if math.gcd(g1, p1 * q1) != 1:
        continue
    if pow(g1, (p1 - 1) // 2, p1) != p1 - 1:
        continue
    if pow(g1, (q1 - 1) // 2, q1) != q1 - 1:
        continue
    break

g2 = random.randint(2, p2 - 2)
d = random.randint(2, p2 - 2)
beta = pow(g2, d, p2)

pt = bytes_to_long(os.urandom(127 - len(FLAG)) + FLAG)
tmp = random.randint(2, p2 - 2)
c1 = pow(g2, tmp, p2)
c2 = pow(beta, tmp , p2) * pt % p2

hint = p2 >> 1024
print(f"{n = }")
print(f"{c1 = }")
print(f"{c2 = }")
print(f"{hint = }")

while True:
    inp1 = int(input("c1 = ").strip())
    inp2 = int(input("c2 = ").strip())
    m = pow(inp1, -d, p2) * inp2 % p2
    print(pow(g1, m, n))


