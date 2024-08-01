with open("pusheen.txt", "r") as f:
    ooo = f.readlines()
    ooo.append("\n")
    print(len(ooo))
    assert len(ooo) % 16 == 0

a = "".join(ooo[0: 16])
b = "".join(ooo[16: 32])
print(a)
print(b)
print(len(a))
print(len(b))
for i in range(521):
    if a[i] != b[i]:
        print(i)
        print(a[i])
        break
difference = a[31]

for i in range(0, len(ooo), 16):
    res = "".join(ooo[i: i + 16])
    if res[31] == difference:
        print("0",end="")
    else:
        print("1",end="")
print("")
from Crypto.Util.number import long_to_bytes

res = int("010001100100110001000001010001110111101101010000011101010111001101101000011001010110010101101110001000000100111101001001010011110100111101001111010010010100100101001111010011110100100101001111010011110100100101001001010011110100111101001111010010010100111101001111010011110100111101001111010010010100111101001001010011110100111101001111010010010100100101001001001000000100001101110101011101000110010101111101",2)
print(long_to_bytes(res).decode())