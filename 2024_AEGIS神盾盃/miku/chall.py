from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

with open('flag.png', 'rb') as f:
    miku = 1
    for _ in range(39):
        miku *= getPrime(39)

    negi = 0x10001
    kotoba = os.urandom(32)

    roller = AES.new(kotoba, AES.MODE_CBC)
    with open('flag.png.enc', 'w') as g:
        g.write(roller.iv.hex())
        g.write('\n')
        g.write(roller.encrypt(pad(f.read(), AES.block_size)).hex())

    with open('hint.txt', 'w') as g:
        g.write(f'miku = {miku}\n')
        g.write(f'negi = {negi:x}\n')
        g.write(f'kotoba = {pow(bytes_to_long(kotoba), negi, miku)}')
