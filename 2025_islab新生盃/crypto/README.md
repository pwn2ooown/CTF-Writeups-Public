# Crypto

## Crypto Party

這應該是最爛的一題了

```
You find a note at the party that looks like ciphertext:

==gVftUYTV0TQFTeuR1c0J2XK9Fc1dGexh0Rt9WfNB3R291Z7Z2Y
Curious, you show it to the party host. He chuckles and says, "The secret was made by applying six encryption/encoding steps in the following order:"

STEP① Affine Cipher
STEP② Vigenère
STEP③ Caesar
STEP④ Rail Fence Cipher
STEP⑤ Base64
STEP⑥ String Reverse
```

去 cyberchef 拉一下就能還原到第四部會長得像 `co1mfGPH{qOxggEu_pS_vJa_GbKtps_TMnVy}`

但是前面三個的 key 是 unknown 所以要開始通靈了

注意到Vigenère -> Caesar 是被吸收的因為都是位移加密

那我們知道一個位子在經過 affine 會變成 `P' = (a * P + b) mod 26`
再 Vigenère `C = (P' + k_i) mod 26`

然後再經過一陣通靈可以求出 key 長度是 3 以及 a 還有 b 還有算出 Vigenère 的 key

```python
def decrypt_combined_cipher(ciphertext: str) -> str:
    """
    解密經過「仿射 -> 維吉尼亞」複合加密的密文。
    此函數使用預先分析得到的金鑰參數。
    """
    
    # ------------------- 預先分析得到的金鑰參數 -------------------
    # 仿射密碼乘數 a 的模26乘法反元素
    a_inverse = 15
    
    # 等效的維吉尼亞金鑰 (複合位移量 B = b + k_i)
    key_b = [24, 18, 12]
    key_len = len(key_b)
    # -----------------------------------------------------------

    # 從已知明文部分 "is1abCTF" 計算起始的字母索引
    # "isabCTF" 總共有 7 個字母
    alpha_index = 7
    
    decrypted_text = "is1abCTF{"
    
    # 密文中需要解密的部分
    encrypted_part = "qOxggEu_pS_vJa_GbKtps_TMnVy"

    for char in encrypted_part:
        # 檢查字元是否為英文字母
        if 'a' <= char.lower() <= 'z':
            is_upper = char.isupper()
            
            # 將字母轉換為 0-25 的數字
            # C for Ciphertext character value
            if is_upper:
                c_val = ord(char) - ord('A')
            else:
                c_val = ord(char) - ord('a')
            
            # 根據目前的字母索引，取得對應的位移金鑰
            shift = key_b[alpha_index % key_len]
            
            # 應用解密公式: P = a⁻¹ * (C - B_i) mod 26
            # P for Plaintext character value
            p_val = (a_inverse * (c_val - shift)) % 26
            
            # 將解密後的數字轉回字母，並還原大小寫
            if is_upper:
                decrypted_char = chr(p_val + ord('A'))
            else:
                decrypted_char = chr(p_val + ord('a'))
            
            decrypted_text += decrypted_char
            
            # 字母索引加一，為下一個字母做準備
            alpha_index += 1
        else:
            # 如果不是字母 (例如 '_')，直接附加到結果中
            decrypted_text += char
            
    # 加上結尾的括號
    decrypted_text += "}"
    
    return decrypted_text

# --- 主程式執行區 ---
if __name__ == "__main__":
    # 已知的完整密文
    full_ciphertext = "co1mfGPH{qOxggEu_pS_vJa_GbKtps_TMnVy}"
    
    # 執行解密
    flag = decrypt_combined_cipher(full_ciphertext)
    
    print(f"原始密文: {full_ciphertext}")
    print(f"解密 Flag: {flag}")
```

爛題 `¯\_(ツ)_/¯` 不過我懷疑這題有很簡單的解法不然怎麼一堆人解

或是有人在 share flag?

## MITM

Since p-1 is smooth, Pohlig-Hellman can compute the discrete log efficiently.

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import sympy
import hashlib

p = 155214169224186174245759019817233758959712483609876556421679567759735878173206273314271380424223420051598278563855517852997101246947883176353747918435174813511975576536353646684036755728974423538143090186411163821396091652013002565116673426504500657692938270440503451481091007910872038288051399770068237950977
g = 5
A = 24126573438929516944661872788158819371065146350692792884683295327238738557471054692543815345984135204612246103570946031263555360060204100672504858546593795142635009231389701378856979682645489518003284745954378690249465168862782314668693228551924534299276467443443393671282493766536563304005336765380120486801
B = 28185916776379980430839395101046151783562827247095808519029117903859608155748920613744225030479670168498741544252438695183463705295578456576270093983349388913369780421918605776826638697501215735795159947272825924382460667752341611128457970043662601357663635848681507656711255557701250916304947857522011099599
a = sympy.ntheory.discrete_log(p, A, g)
s = pow(B, a, p)
secret_bytes = s.to_bytes((s.bit_length() + 7) // 8, 'big')
symmetric_key = hashlib.sha256(secret_bytes).digest()

enc_alice = "03d2bc679747ab70e14f98cb9e32a6e0c56f84e57f1599dd028cf255bca0a8c0ee015bc0f13826dc32c2d3b231048ccc4653e3ba119ddafec61ad35977bbb0b9"
iv_alice = bytes.fromhex(enc_alice[:32])
ct_alice = bytes.fromhex(enc_alice[32:])

cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv_alice))
decryptor = cipher.decryptor()
dec_alice = decryptor.update(ct_alice) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
plain_alice = unpadder.update(dec_alice) + unpadder.finalize()
plain_alice = plain_alice.decode('utf-8')

enc_bob = "cafbee2cb5a3259280c5a34772a302700cc4d80ddc6e4f6459146d6d9ae0f6117f9967cd3c9bf9aca62c003b4201555cfcf94f94477d6930ee7eb2e26a18203421e27c10e1b445e9cc333086417a68b7e0142f4b951224800d8e4e9ae85e7d62"
iv_bob = bytes.fromhex(enc_bob[:32])
ct_bob = bytes.fromhex(enc_bob[32:])

cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv_bob))
decryptor = cipher.decryptor()
dec_bob = decryptor.update(ct_bob) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
plain_bob = unpadder.update(dec_bob) + unpadder.finalize()
plain_bob = plain_bob.decode('utf-8')

print(plain_alice)
print(plain_bob)
```

## See if your AI can crack this

nonce reuse attack

```python
# Curve parameters for secp256k1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (Gx, Gy)

# Public key coordinates (from provided X and Y)
X_hex = 'd1acf58809885440aa21f2889bf2f55c8a3cda842f0369dcc51fc5f32245c34b'
Y_hex = '473951cf71f9bebe04b8e72fd09efbe76706b439584bc5212220c96bb3f23216'
pubkey_xy = (int(X_hex, 16), int(Y_hex, 16))

def modinv(x, m):
    return pow(x, -1, m)

def ec_add(P, Q):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P == Q:
        lam = (3*x1*x1 + a) * modinv(2*y1 % p, p) % p
    else:
        lam = (y2 - y1) * modinv((x2 - x1) % p, p) % p
    x3 = (lam*lam - x1 - x2) % p
    y3 = (lam*(x1 - x3) - y1) % p
    return (x3, y3)

def ec_mul(k, P):
    R = None
    Q = P
    while k:
        if k & 1:
            R = ec_add(R, Q)
        Q = ec_add(Q, Q)
        k >>= 1
    return R

def verify(msg_hash_int: int, r: int, s: int, pubkey_xy: tuple[int,int]) -> bool:
    """
    Return True iff the signature (r, s) validates for the given message hash and public key.
    This is a straight verification routine referencing SEC 1, §4.1.4.
    """
    if not (1 <= r < n and 1 <= s < n):
        return False
    w = modinv(s, n)
    u1 = (msg_hash_int * w) % n
    u2 = (r * w) % n
    X = ec_add(ec_mul(u1, G), ec_mul(u2, pubkey_xy))
    if X is None:
        return False
    xR = X[0] % n
    return xR == r

import csv

def parse_csv(filename: str) -> list[tuple[int, int, int]]:
    """
    Parse a CSV file with columns: msg_hash, r, s (hex strings).
    Assumes optional header row; skips it if present.
    Returns list of (msg_hash_int, r_int, s_int) tuples.
    """
    signatures = []
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        # Optionally skip header (check if first row looks like headers)
        first_row = next(reader)
        if first_row[0].lower().startswith('msg_hash'):  # Assume header if starts with 'msg_hash'
            pass  # Already consumed, proceed to data
        else:
            # No header; process first row as data
            h = int(first_row[0], 16)
            r = int(first_row[1], 16)
            s = int(first_row[2], 16)
            signatures.append((h, r, s))

        for row in reader:
            if row:  # Skip empty rows
                h = int(row[0], 16)
                r = int(row[1], 16)
                s = int(row[2], 16)
                signatures.append((h, r, s))
    return signatures

def recover_private_key(sig1, sig2, n):
    h1, r, s1 = sig1
    h2, _, s2 = sig2  # Assumes same r
    if r == 0 or s1 == s2 or s1 == 0 or s2 == 0:
        raise ValueError("Invalid signatures for recovery")
    diff_s = (s1 - s2) % n
    diff_h = (h1 - h2) % n
    k = (diff_h * modinv(diff_s, n)) % n
    d = ((s1 * k - h1) * modinv(r, n)) % n
    return d

def find_and_recover_private_key(csv_filename: str, pubkey_xy: tuple[int,int]):
    signatures = parse_csv(csv_filename)

    # Group signatures by r
    from collections import defaultdict
    groups = defaultdict(list)
    for sig in signatures:
        h, r, s = sig
        groups[r].append(sig)

    recovered_d = None
    for r, group in groups.items():
        if len(group) >= 2:
            # Take first two signatures with same r
            sig1 = group[0]
            sig2 = group[1]
            try:
                d = recover_private_key(sig1, sig2, n)
                # Verify if this d generates the correct pubkey
                derived_pub = ec_mul(d, G)
                if derived_pub == pubkey_xy:
                    # Optionally verify all signatures in the group
                    all_valid = all(verify(h, r_sig, s, pubkey_xy) for h, r_sig, s in group)
                    if all_valid:
                        recovered_d = d
                        print(f"Recovered private key: {hex(d)}")
                        print("All signatures verified successfully.")
                        return recovered_d  # Return on first successful recovery
                    else:
                        print("Derived pubkey matches, but not all signatures verify.")
                else:
                    print("Derived pubkey does not match the given pubkey.")
            except ValueError as e:
                print(f"Error recovering from group with r={hex(r)}: {e}")

    if recovered_d is None:
        print("No suitable pairs found for recovery.")
    return recovered_d

# Example usage: Replace 'your_signatures.csv' with your actual CSV file path
if __name__ == "__main__":
    csv_file = 'signatures.csv'  # Change this to your CSV file
    private_key = find_and_recover_private_key(csv_file, pubkey_xy)
    if private_key:
        print(f"Final recovered private key (hex): {hex(private_key)}")

# is1abCTF{6bf908ba4975f133b8ccfceed54faa92958729979216e38cd7e5d7ece7e477a8}
```

## SurfSalt VPN

`heymrsalt` is the Vigenère key

```
The Unbreakable Code: The Age of the Vigenère Cipher

For centuries, the art of cryptography was a constant battle between concealment and revelation. Since the era of Julius Caesar, simple substitution ciphers dominated the world of secret messages. In these systems, a letter was consistently replaced by another, a simple trick that created a facade of security. However, by the 9th century, brilliant minds in the Arab world had perfected frequency analysis, a method of counting letter occurrences to systematically break these codes. For hundreds of years, code makers could only create puzzles that, with enough time and intellect, codebreakers could invariably solve. Secrecy was fragile and temporary.

Feeling like your secrets aren't safe? Wishing for an uncrackable solution in your daily life? Introducing "SurfSalt VPN™" – the revolutionary new app that uses advanced… well, not quite Vigenère, but it’s still pretty good! SurfSalt VPN is super secure, like you're encrypting it for yourself: is1abCTF{SurfSalt_VPN_is_SuCh_4_GreAt_DeaL}. Download today for 15% off your first year of ultimate digital privacy! (Offer not valid on actual military-grade encryption.) Now, back to our regularly scheduled history!

This all began to change in 1553, with Giovan Battista Bellaso's description of a new, revolutionary system, later misattributed to and named after the French diplomat Blaise de Vigenère. The Vigenère cipher was a true paradigm shift. Instead of using one static cipher alphabet, it employed a keyword to shift between 26 different possible alphabets throughout the message. A letter like 'e' might be encrypted as 'L' in one instance and 'W' in the next, effectively flattening the statistical frequency patterns that codebreakers relied upon.

The Vigenère cipher was so powerful that it was deemed practically unbreakable. For three centuries, it earned the formidable nickname "le chiffrage indéchiffrable"—the indecipherable cipher. Its complexity provided an unprecedented level of security for military, diplomatic, and personal correspondence. This cryptographic stronghold remained secure until 1854, when Charles Babbage, a visionary English mathematician, finally developed a systematic method to crack it. The Vigenère cipher marked a new epoch in cryptography, introducing a complexity that fundamentally altered the balance of power between those who hide secrets and those who seek them.
```
