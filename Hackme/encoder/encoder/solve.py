import base64
import string
import sys

def rot13(s):
    return s.translate(str.maketrans(string.ascii_uppercase + string.ascii_lowercase,
        string.ascii_uppercase[13:] + string.ascii_uppercase[:13] +
        string.ascii_lowercase[13:] + string.ascii_lowercase[:13]))

def base64dec(s):
    return base64.b64decode(s).decode('utf-8')

def hex(s):
    return bytes.fromhex(s).decode('utf-8')

def upsidedown(s):
    return s.translate(str.maketrans(string.ascii_lowercase + string.ascii_uppercase,
        string.ascii_uppercase + string.ascii_lowercase))

def my_base64(s):
    return ''.join(s.encode('base64').split())

with open("flag.enc","r") as f:
    flag = f.read()
    # print(flag)
    # for i in range(int(sys.argv[1])):
    for i in range(47):
        c = int(flag[0])
        flag = flag[1:]
        if c == 0:
            flag = rot13(flag)
            print("rot13")
        elif c == 1:
            flag = base64dec(flag)
            print("base64 decode")
        elif c == 2:
            flag = hex(flag)
            print("unhex")
        elif c == 3:
            flag = upsidedown(flag)
            print("downsideup")
        else:
            print("error")
            break
    print(flag)
    # FLAG{???}
