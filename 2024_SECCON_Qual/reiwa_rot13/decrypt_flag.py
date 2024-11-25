
encyprted_flag =  b"\xdb'\x0bL\x0f\xca\x16\xf5\x17>\xad\xfc\xe2\x10$(DVsDS~\xd3v\xe2\x86T\xb1{xL\xe53s\x90\x14\xfd\xe7\xdb\xddf\x1fx\xa3\xfc3\xcb\xb5~\x01\x9c\x91w\xa6\x03\x80&\xdb\x19xu\xedh\xe4"
key = 474273460180197900644210
from Crypto.Util.number import *
import hashlib
from Crypto.Cipher import AES
key = hashlib.sha256(long_to_bytes(key)).digest()
cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(encyprted_flag))