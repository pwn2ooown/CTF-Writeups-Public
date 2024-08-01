from pwn import *
import sys
# context.log_level = "debug"


if len(sys.argv) == 1:
    r = process("./chal")
    #gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.interactive()

'''
pwndbg> p __elf_set___libc_atexit_element__IO_cleanup__
$1 = (const void *) 0x7ffff7e409d0 <_IO_cleanup>
pwndbg> p &__elf_set___libc_atexit_element__IO_cleanup__
$2 = (const void **) 0x7ffff7f8b9d8 <__elf_set___libc_atexit_element__IO_cleanup__>
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
    0x555555554000     0x555555555000 r--p     1000      0 /home/kali/CTF/SCIST/Archive/FMT_Advance/chal/share/chal
    0x555555555000     0x555555556000 r-xp     1000   1000 /home/kali/CTF/SCIST/Archive/FMT_Advance/chal/share/chal
    0x555555556000     0x555555557000 r--p     1000   2000 /home/kali/CTF/SCIST/Archive/FMT_Advance/chal/share/chal
    0x555555557000     0x555555558000 r--p     1000   2000 /home/kali/CTF/SCIST/Archive/FMT_Advance/chal/share/chal
    0x555555558000     0x555555559000 rw-p     1000   3000 /home/kali/CTF/SCIST/Archive/FMT_Advance/chal/share/chal
    0x7ffff7dba000     0x7ffff7dbd000 rw-p     3000      0 [anon_7ffff7dba]
    0x7ffff7dbd000     0x7ffff7de3000 r--p    26000      0 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7de3000     0x7ffff7f38000 r-xp   155000  26000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7f38000     0x7ffff7f8b000 r--p    53000 17b000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7f8b000     0x7ffff7f8f000 r--p     4000 1ce000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7f8f000     0x7ffff7f91000 rw-p     2000 1d2000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7f91000     0x7ffff7f9e000 rw-p     d000      0 [anon_7ffff7f91]
    0x7ffff7fc3000     0x7ffff7fc5000 rw-p     2000      0 [anon_7ffff7fc3]
    0x7ffff7fc5000     0x7ffff7fc9000 r--p     4000      0 [vvar]
    0x7ffff7fc9000     0x7ffff7fcb000 r-xp     2000      0 [vdso]
    0x7ffff7fcb000     0x7ffff7fcc000 r--p     1000      0 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7fcc000     0x7ffff7ff1000 r-xp    25000   1000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ff1000     0x7ffff7ffb000 r--p     a000  26000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000  30000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffd000     0x7ffff7fff000 rw-p     2000  32000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffffffde000     0x7ffffffff000 rw-p    21000      0 [stack]
pwndbg> Quit
pwndbg> 
'''