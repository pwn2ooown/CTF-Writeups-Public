from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
import sys


ENCRYPTED_FLAG = b'\x99\xcb\xf3\x9c9\xe5\xc9\x92[r\xf0-n\xb8\xc7\x9d\xda\xd6}\x01\x83\xc8\x9d\xef\xf7\xf37\x8f\xc3\xd0\xd0lR\xfe\xc2\xf6\xb4\r\x18\x97\xe9\xe5\x12\x93D\xdf7\xe6\xa9\xb0m\x1e\xda\xdf\x95\x1bU$U\xbfPo\xf7\xd0\xa0\xd2\xf8\x9f\xd7/\x90c\xc1\x1a8\xef\xadAR\xaf'

# Prompt
print('Welcome to the flag decryptor! (｡･ω･｡)ﾉ♡')
print('Please make a file to store your all answers (in integers).\nMake sure there is not endline at the end.')

print('''The file is has to follow the format below:
<answer[0]>
<answer[1]>
<answer[2]>
...
<answer[N]>''')

print('''Here is an example that satisfies the format:
251
5
2
3
...
63''')
path = input('Please enter the file path of answer: ')

try:
    with open(path, 'r') as fp:
        answers = list(map(int, fp.read().split('\n')))
except:
    print('[-] Error: Invalid path. ﾋﾞｪ──･ﾟ･(｡>д<｡)･ﾟ･──ﾝ!!')
    sys.exit(1)

# Key Derivation
sha256_obj = SHA256.new(data=bytes(answers))
key = sha256_obj.digest()
print(f'[*] Derived Key (May not able to decrypt): {sha256_obj.hexdigest()}')

# Flag decryption
try:
    aes_obj = AES.new(key=key, mode=AES.MODE_CBC, iv=bytes(answers[:16]))
    flag = unpad(aes_obj.decrypt(ENCRYPTED_FLAG), AES.block_size)
    print(f'[+] Congrats （＊´・∀・＊）! Here is your flag: {flag.decode()}!')

except UnicodeDecodeError:
    print('[-] Error: Invalid flag. ﾋﾞｪ──･ﾟ･(｡>д<｡)･ﾟ･──ﾝ!!')
    sys.exit(1)