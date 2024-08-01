with open("xor","rb") as f:
    res = f.read()
print(res)
key = b"HACKMEPLS"
for i in range(len(res)):
    print(chr(res[i]^key[i%len(key)]),end="")