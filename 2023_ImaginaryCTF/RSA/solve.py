import math
from Crypto.Util.number import long_to_bytes
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % m

def decrypt_RSA(ciphertext, p, q, e):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = mod_inverse(e, phi_n)
    print(n)
    print(d)
    plaintext = pow(ciphertext, d, n)
    return plaintext

p = 0x00feafbc97cdec01bf5afe8abe2802d8f4ee217c63740c887c72920431108e993dc6f3cfeed6a41830435cfa9cc08d26e01fb3dfc5c6df83a488e8df3d89762b6d
q = 0x00ca58fb227d61c1a037b372f548f304e464eabea4dc6edbca84f96b589ec28b837f554fb3072334069b181c5a39711bc53b11651c3219e003cb9fe5abb36a1bcf
e = 65537
with open('flag.enc','rb') as f:
    data = f.read()
    ciphertext = int.from_bytes(data, byteorder='big')
    # print(ciphertext)
decrypted_file_content = decrypt_RSA(ciphertext, p, q, e)
print(long_to_bytes(decrypted_file_content))
print(0x00c94f31113aa7f5dfce22d7c5e2a9f82553556e0aa4096aa86688c180df33472c1a2316494b7deddcc43c1d24ca2599b74bfffa94734cbdc866126cb514465792f153026d6921b48d52082c40c64a9b45281621e49c77cf9e77824e5177f04d7da70a03b53f1a755db783a9b6b89e747f6a06f577aff8722ca8eb0e5bcf439c23)
