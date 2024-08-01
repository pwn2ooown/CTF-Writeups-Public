#! /usr/bin/python3
from Crypto.Cipher import AES
from hashlib import sha256
import os

from secret import FLAG

token = os.urandom(8)
iv = os.urandom(16)
key = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
print(iv.hex() + cipher.encrypt(token.hex().encode()).hex())
print("Hint: ", sha256(token).hexdigest())
while True:
    print("1: Send")
    print("2: Guess")
    print("3: Exit")
    inp = int(input())
    if inp == 1:
        inp = bytes.fromhex(input("Message(hex): "))
        iv = inp[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        m = cipher.decrypt(inp[16:]).decode()
        try:
            m = bytes.fromhex(m)
            print("Well received")
        except:
            print("Invalid")
    elif inp == 2:
        inp = input("Token(hex): ")
        if inp == token.hex():
            print("Your FLAG: " + FLAG.decode())
        exit(0)
    else:
        print("Bye~")
        exit(0)