from pwn import *

r = remote("lotuxctf.com", 10000)

print(r.recvline().decode())

low_num = 0
high_num = 10000000
guess = 0
number_found = False
response = ""
while not number_found:
    if("lower" in response):
        high_num = int(guess)
    elif("higher" in  response):
        low_num = int(guess)
    guess = str((high_num+low_num) // 2)
    print(guess)
    r.sendline(guess.encode())
    response = r.recvline().decode()
    print(response, end='')
    if "clear" in response:
        number_found = True
print(r.recvline().decode(), end='')
for i in range(101):
    question = r.recvuntil(b'=')[:-1].decode()
    ans = eval(question)
    print(f"Question{i+1}:"+question+f"={ans}")
    r.sendline(str(ans).encode())
print(r.recvline().decode())
    
r.close()