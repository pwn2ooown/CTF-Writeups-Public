# Actually I solved it by hand...

from pwn import *
import sys
context.log_level = "debug"
import time

if len(sys.argv) == 1:
    r = process("./chal")
    #gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    sys._exit(1)
r.recvuntil(b"Let's go!\n")
for i in range(30):
    res = r.recvuntil(b'\n').decode()
    res = res.replace('\t','')
    res = res.replace(' ','')
    res = res.replace('\n','')
    print(res)
    r.sendline(str(eval(res))) # Don't use this
    time.sleep(1)

r.interactive()