# Reverse

## Baby Reverse

annoy.zip

```python
target = [
0x36, 0xBF, 0x21, 0xCD, 0xAC, 0x9A, 0x9C, 0x3A,
0x0A, 0xA6, 0x85, 0xE2, 0x2E, 0xC2, 0x0D, 0xC9,
0x27, 0x9C, 0xAB, 0x9F, 0x8D, 0xA6, 0xA4, 0xE2,
0x34, 0xB5, 0x8E, 0xD1, 0x04, 0xEA, 0x0B, 0xB5,
0xAE, 0x51, 0x1A, 0xEA, 0x8C, 0xCB, 0x2E, 0xBC,
0xA4, 0xE9, 0x35, 0x4B, 0x2C, 0x4D, 0x29
]

def rol1(b):
    return ((b << 1) & 0xFF) | ((b >> 7) & 0x01)

pre4 = [rol1(b) for b in target]

def inv_crypt3(data):
    res = []
    for i in range(len(data)):
        b = data[i]
        mod = i % 3
        if mod == 0:
            res.append((b - 5) % 256)
        elif mod == 1:
            res.append((b + 9) % 256)
        else:
            res.append(b ^ 0x4D)
    return res

pre3 = inv_crypt3(pre4)

def inv_crypt2(data):
    res = []
    for i in range(len(data)):
        b = data[i]
        if (i % 2) == 0:  # even
            res.append((b + 17) % 256)
        else:
            res.append((b - 38) % 256)
    return res

pre2 = inv_crypt2(pre3)

def inv_crypt1(data):
    res = []
    for i in range(len(data)):
        res.append(data[i] ^ 0x11)
    return res

password_bytes = inv_crypt1(pre2)
password = ''.join(chr(x) for x in password_bytes)
print(password)
```

## Basic Crackme

crackme.exe

```python
v2 = [0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]

def sub_240(x):
    return (16 * v2[x & 0xF]) | v2[x >> 4]

targets = [
-433789332,
40534546,
1815012958,
-695967214,
1819172522,
-1396925846,
-429986636,
-324766550,
-1031501274,
-1061109718
]

dest = [0] * 40

for j in range(10):
    t = targets[j] & 0xFFFFFFFF
    byte0 = t & 0xFF
    byte1 = (t >> 8) & 0xFF
    byte2 = (t >> 16) & 0xFF
    byte3 = (t >> 24) & 0xFF
    dest[4*j] = sub_240(byte0)
    dest[4*j + 1] = sub_240(byte3)
    dest[4*j + 2] = sub_240(byte1)
    dest[4*j + 3] = sub_240(byte2)

key = ''.join(chr(d) for d in dest[:37])
print("Key:", key)
print("Padded bytes:", dest[37], dest[38], dest[39])

xor_stream = [64,1,86,74,39,16,6,5,1,102,87,21,60,14,8,22,61,79,20,17,103,5,56,98,97,87,127,37,37,114,26,85,60,28,11,18,41]

v4 = [dest[i] ^ xor_stream[i] for i in range(37)]

for i in range(37):
    c = v4[i]
    if 65 <= c <= 90:
        v4[i] = ((c - 52) % 26) + 65
    elif 97 <= c <= 122:
        v4[i] = ((c - 84) % 26) + 97

flag = ''.join(chr(c) for c in v4)
print("Flag:", flag)
```

### Half-Baked Image Format

muzi.tar

AI 大法好

```python
from PIL import Image
import numpy as np
import crc8
import sys

def main():
    """主選單函式，提供使用者操作選項。"""
    # 使用 try-except 以處理使用者中斷程式 (Ctrl+C) 的情況
    try:
        inp = input("""
                      Welcome to the is1ab Image Program
                      It can convert images to MUZIs
                      It will also display MUZIs

                      [1] Convert Image to MUZI
                      [2] Display MUZI from file

                      Enter your choice: """)
        match inp:
            case "1":
                start_conv()
            case "2":
                display() # 從 MUZI 檔案還原成圖片
            case _:
                print("Invalid option, exiting.")
                return 0
    except (KeyboardInterrupt, EOFError):
        print("\nProgram interrupted by user. Exiting.")
        sys.exit(0)
    return 0

def start_conv():
    """將標準圖片格式 (如 PNG, JPG) 轉換為 .muzi 格式。"""
    try:
        file = input("Enter the path to your image you want converted to a MUZI file:\n")
        out = input("Enter the path you’d like to write the MUZI to:\n")
        
        print("Opening image...")
        img = Image.open(file).convert("RGB") # 確保圖片是 RGB 格式
        w, h = img.size
        print(f"Image loaded: {w}x{h}")

        # MUZI 檔案格式的檔頭
        write = [
            b'\x4D', b'\x55', b'\x5A', b'\x49', b'\x00', b'\x01', b'\x00', b'\x02'
        ]

        # 寫入寬度和高度 (各 4 bytes)
        write.extend(list(w.to_bytes(4, 'little')))
        write.extend(list(h.to_bytes(4, 'little')))
        
        # WIFI 區塊標記
        write.extend([b'\x57', b'\x49', b'\x46', b'\x49'])
        
        print("Processing color channels...")
        # 逐一處理 R, G, B channel
        channels = [('R', 'DATR'), ('G', 'DATG'), ('B', 'DATB')]
        for idx, (channel_name, marker) in enumerate(channels):
            print(f"  - Writing {channel_name} channel data...")
            for i in range(h): # 逐行處理
                # 每一行的資料區塊標頭
                dat = [m.encode('ascii') for m in marker]
                # 提取該行的 pixel data
                row_data_bytes = [img.getpixel((j, i))[idx].to_bytes(1) for j in range(w)]
                dat.extend(row_data_bytes)
                # 計算並附加 CRC8 checksum
                dat.append(getCheck(row_data_bytes))
                write.extend(dat)

        # 檔案結束標記
        write.extend([b'\x44', b'\x41', b'\x54', b'\x45']) # DATE

        print(f"Writing data to {out}...")
        with open(out, "wb") as f: # 使用 "wb" (write binary) 模式確保覆寫檔案
            for b in write:
                # 確保寫入的是 bytes
                if isinstance(b, int):
                    f.write(b.to_bytes(1))
                else:
                    f.write(b)
        
        print("Conversion successful! ✨")

    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return 0

def display():
    """從 .muzi 格式檔案還原成圖片並儲存。"""
    try:
        file = input("Enter the path to your MUZI file:\n")
        out = input("Enter the path you’d like to write the output image to (e.g., output.png):\n")

        print(f"Reading MUZI file: {file}")
        with open(file, "rb") as f:
            # 驗證檔頭
            header = f.read(8)
            if header[:4] != b'MUZI':
                print("Error: Not a valid MUZI file.")
                return

            # 讀取寬高
            w = int.from_bytes(f.read(4), 'big')
            h = int.from_bytes(f.read(4), 'big')
            print(f"Image dimensions found: {w}x{h}")

            # 驗證 WIFI 標記
            if f.read(4) != b'WIFI':
                print("Error: WIFI marker not found or corrupted.")
                return

            # 準備一個 NumPy array 來存放像素資料
            pixel_data = np.zeros((h, w, 3), dtype=np.uint8)

            # 讀取 R, G, B channel
            channels = [('R', b'DATR'), ('G', b'DATG'), ('B', b'DATB')]
            for idx, (channel_name, expected_marker) in enumerate(channels):
                print(f"  - Reading {channel_name} channel data...")
                for i in range(h): # 逐行讀取
                    marker = f.read(4)
                    if marker != expected_marker:
                        print(f"Error: Corrupted data chunk for row {i} in channel {channel_name}.")
                        return
                    
                    # 讀取一整行的 pixel data 和 checksum
                    row_data = f.read(w)
                    checksum_from_file = f.read(1)

                    # 驗證 checksum
                    calculated_checksum = crc8.crc8(row_data).digest()
                    if checksum_from_file != calculated_checksum:
                        print(f"Warning: Checksum mismatch in row {i} of {channel_name} channel!")
                    
                    # 將資料填入 NumPy array
                    pixel_data[i, :, idx] = np.frombuffer(row_data, dtype=np.uint8)
            
            # 驗證檔案結束標記
            if f.read(4) != b'DATE':
                print("Warning: End of file marker 'DATE' not found.")

            print("Reconstructing image from pixel data...")
            # 從 NumPy array 建立 Pillow 圖片物件
            img = Image.fromarray(pixel_data, 'RGB')
            img.save(out)
            print(f"Image successfully saved to {out}! ✅")

    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def getCheck(datr):
    """計算給定 byte list 的 CRC8 checksum。"""
    # 將 bytes list 合併成一個 bytes object
    data_bytes = b''.join(datr)
    # 計算 crc8 並回傳 bytes 格式的 checksum
    return crc8.crc8(data_bytes).digest()

if __name__ == '__main__':
    main()
```

## Image Encryptor

encryptor.zip

主要的加密在 `sub_14000195D`

邏輯就是他有一個 PRNG Gen state 後然後 state 去 mod 32 當作一個 function_pointer_table[32] 的 index (32個加密函數) (當然 state 其他 bits 有其他用途)

用那個加密函數處理兩個兩個 byte，依次還原就好

```python
import sys
from pathlib import Path
from typing import Callable, Tuple

# Fixed constants derived from the binary
SEED = 0x121AB312  # sub_140001460 seed
MULTIPLIER = 16807  # sub_140001473 multiply
MASK32 = 0xFFFFFFFF
HEADER_QWORD_LE = 0x4654436261317349  # fwrite of this 8-byte little-endian value
HEADER_BYTES = HEADER_QWORD_LE.to_bytes(8, byteorder="little")  # b"Is1abCTF"


def rotate_left_8(value: int, count: int) -> int:
	count &= 7
	if count == 0:
		return value & 0xFF
	return ((value << count) | (value >> (8 - count))) & 0xFF


def rotate_right_8(value: int, count: int) -> int:
	count &= 7
	if count == 0:
		return value & 0xFF
	return ((value >> count) | (value << (8 - count))) & 0xFF


def prng_next(state: int) -> int:
	"""Advance PRNG: state = state * 16807 (mod 2^32). Return new state."""
	return (state * MULTIPLIER) & MASK32


def inverse_transform(index: int, param: int, value: int) -> int:
	"""Invert funcs_140001954[index](a1, param) for one byte."""
	p = param & 0xFF
	if index == 0:  # y = a2 ^ a1
		return p ^ value
	elif index == 1:  # y = a1 + a2
		return (value - p) & 0xFF
	elif index == 2:  # y = a1 - a2
		return (value + p) & 0xFF
	elif index == 3:  # y = ~a1
		return (~value) & 0xFF
	elif index == 4:  # y = ROR(a1, p&7)
		return rotate_left_8(value, p & 7)
	elif index == 5:  # y = ROL(a1, p&7)
		return rotate_right_8(value, p & 7)
	elif index == 6:  # y = swap_nibbles(a1)
		return ((value << 4) | (value >> 4)) & 0xFF
	elif index == 7:  # y = a1 ^ (a2 >> 4)
		return value ^ (p >> 4)
	elif index == 8:  # y = (a2 & 0xF) ^ a1
		return value ^ (p & 0xF)
	elif index == 9:  # y = ~(a2 ^ a1)
		return (p ^ ((~value) & 0xFF)) & 0xFF
	elif index == 10:  # y = a1 ^ 0x55
		return value ^ 0x55
	elif index == 11:  # y = a1 ^ 0xAA
		return value ^ 0xAA
	elif index == 12:  # y = (a2 >> 4) + a1
		return (value - (p >> 4)) & 0xFF
	elif index == 13:  # y = a1 - (a2 & 0xF)
		return (value + (p & 0xF)) & 0xFF
	elif index == 14:  # y = ~(a1 + a2)
		return ((~value) - p) & 0xFF
	elif index == 15:  # y = a2 - a1
		return (p - value) & 0xFF
	elif index == 16:  # y = a1 ^ (a1 >> 4)
		# y_high = h, y_low = l ^ h -> x = (h<<4) | (l^h)
		h = (value >> 4) & 0xF
		l = value & 0xF
		return ((h << 4) | (l ^ h)) & 0xFF
	elif index == 17:  # y = (a1 << 4) ^ a1
		# y_high = h ^ l, y_low = l -> x = ((y_high ^ y_low)<<4) | y_low
		y_high = (value >> 4) & 0xF
		y_low = value & 0xF
		return (((y_high ^ y_low) << 4) | y_low) & 0xFF
	elif index == 18:  # y = ROR(a1,1)
		return rotate_left_8(value, 1)
	elif index == 19:  # y = ROL(a1,1)
		return rotate_right_8(value, 1)
	elif index == 20:  # y = ROR(a1,2)
		return rotate_left_8(value, 2)
	elif index == 21:  # y = ROL(a1,2)
		return rotate_right_8(value, 2)
	elif index == 22:  # y = ROR(a1,3)
		return rotate_left_8(value, 3)
	elif index == 23:  # y = ROL(a1,3)
		return rotate_right_8(value, 3)
	elif index == 24:  # y = a1 ^ ROR(a2,4)
		return value ^ rotate_right_8(p, 4)
	elif index == 25:  # y = a1 + ROL(a2,4)
		return (value - rotate_left_8(p, 4)) & 0xFF
	elif index == 26:  # y = a2 + a1 + 1
		return (value - p - 1) & 0xFF
	elif index == 27:  # y = 5*a1 + a2
		return ((value - p) * 205) & 0xFF  # 5^{-1} mod 256 = 205
	elif index == 28:  # y = 3*a1 + a2
		return ((value - p) * 171) & 0xFF  # 3^{-1} mod 256 = 171
	elif index == 29:  # y = 11*a1 + a2
		return ((value - p) * 163) & 0xFF  # 11^{-1} mod 256 = 163
	elif index == 30:  # y = a1
		return value & 0xFF
	elif index == 31:  # y = a1 + 1
		return (value - 1) & 0xFF
	else:
		raise ValueError(f"Unknown transform index: {index}")


def decrypt_bytes(cipher_bytes: bytes) -> bytes:
	"""Decrypt payload bytes (without header), reversing sub_14000195D."""
	state = SEED
	plain = bytearray()
	i = 0
	length = len(cipher_bytes)
	while i < length:
		# If at least two bytes are available, they are (E(b2), E(b1))
		if i + 1 < length:
			# Generate states s1 for b1 and s2 for b2 (encryption order)
			state = prng_next(state)
			s1 = state
			state = prng_next(state)
			s2 = state

			c2 = cipher_bytes[i]
			c1 = cipher_bytes[i + 1]

			# Decrypt c2 with s2 -> b2
			r2 = (s2 >> 8) & 7
			idx2 = (s2 >> 16) & 0x1F
			p2 = s2 & 0xFF
			t2 = rotate_left_8(c2, r2)  # inverse of final ROR
			b2 = inverse_transform(idx2, p2, t2)

			# Decrypt c1 with s1 -> b1
			r1 = (s1 >> 8) & 7
			idx1 = (s1 >> 16) & 0x1F
			p1 = s1 & 0xFF
			t1 = rotate_left_8(c1, r1)
			b1 = inverse_transform(idx1, p1, t1)

			plain.append(b1)
			plain.append(b2)
			i += 2
		else:
			# Odd tail: only E(b_last) was written using s1
			state = prng_next(state)
			s1 = state
			c1 = cipher_bytes[i]
			r1 = (s1 >> 8) & 7
			idx1 = (s1 >> 16) & 0x1F
			p1 = s1 & 0xFF
			t1 = rotate_left_8(c1, r1)
			b1 = inverse_transform(idx1, p1, t1)
			plain.append(b1)
			i += 1
	return bytes(plain)


def main(argv: list[str]) -> int:
	if not (1 <= len(argv) <= 3):
		print("Usage: python decrypt.py <encrypted_input> [output_file]", file=sys.stderr)
		print("Defaults: input=encrypted_image.jpg, output=decrypted_image.jpg", file=sys.stderr)
		return 1

	in_path = Path(argv[1]) if len(argv) >= 2 else Path("encrypted_image.jpg")
	out_path = Path(argv[2]) if len(argv) >= 3 else Path("decrypted_image.jpg")

	data = in_path.read_bytes()
	if len(data) < 8:
		print("Input too short (no header).", file=sys.stderr)
		return 1

	if data[:8] != HEADER_BYTES:
		print("Warning: header mismatch; attempting decryption anyway.", file=sys.stderr)
		payload = data  # try whole file
	else:
		payload = data[8:]

	plaintext = decrypt_bytes(payload)
	out_path.write_bytes(plaintext)
	print(f"Decryption complete -> {out_path}")
	return 0


if __name__ == "__main__":
	sys.exit(main(sys.argv))
```

## Cat the Flag

running_cat.zip

Gameboy 逆向

Tool: https://github.com/visualboyadvance-m/visualboyadvance-m
https://github.com/Gekkio/GhidraBoy

我是完全看不懂 Gameboy 啦，所以很大一部分都是跟 AI 一起看的

可以注意到 FUN_0516 看起來像是記錄某種按鍵的 sequence 並且 FUN_031d 會跟 DAT_023a 去做比較

然後 FUN_0362 就是根據按鍵的 sequence 把 flag 解出來，用 debugger 直接把 memory 0x023a 拉出來是 2, 1, 4, 6, 5, 5, 3, 2, 4, 1

再請 AI 通靈一下把 decryption 給寫出來就好了

```python
def decrypt_flag():
    """
    此腳本模擬了從 Game Boy ROM 反編譯出的 FUN_0362 函式的解密邏輯。
    它使用已知的加密資料 (acStack_56) 和密碼金鑰來還原隱藏的旗標 (FLAG)。
    """
    
    # 1. 加密資料 (Encrypted Data)
    # 這是從 FUN_0362 函式中的 acStack_56 陣列提取的。
    # C 語言中的 char 型別是有符號的，這裡將其轉換為 Python 能處理的 16 位元無符號整數。
    # 例如：C 中的 char -0x26 (十進位 -38) 等於位元組 0xDA。
    # 每個字元由兩個位元組表示（高位元組，低位元組）。
    data_s8 = [
        -0x26, 0, 0xde, 0, 0x67, 0, 0x34, 0, 0x24, 0, 5, 0, 3, 0, -9, 0, 0x31, 0, -102, 0,
        -43, 0, -60, 0, 0x39, 0, 0x36, 0, 0x2f, 0, 0x35, 0, 8, 0, -43, 0, 100, 0, -38, 0,
        -20, 0, -44, 0, 100, 0, 0x20, 0, 0x19, 0, 5, 0, 99, 0, -124, 0, 0x15, 0, -102, 0,
        -43, 0, -98, 0, 0x15, 0, 0x1f, 0, 0x2a, 0, 0x72, 0, 0x30, 0, -110, 0, 0x57, 0,
        -116, 0, -50,0
    ]

    encrypted_words = []
    for i in range(0, len(data_s8), 2):
        # 將 C 的 signed char 轉換為 unsigned byte
        low_byte = data_s8[i] & 0xFF
        high_byte = data_s8[i+1] & 0xFF
        # 組合為 16 位元整數
        word = (high_byte << 8) | low_byte
        encrypted_words.append(word)
    print(encrypted_words)
    # 2. 金鑰 (Key)
    # 這是我們從記憶體 dump 中找到的 10 個按鍵序列所對應的數字。
    # DAT_023a 拉出來的
    key = [2, 1, 4, 6, 5, 5, 3, 2, 4, 1]

    # 3. 解密演算法 (Decryption Algorithm)
    decrypted_flag = ""
    for i, word in enumerate(encrypted_words):
        # 使用模數運算 (%) 來循環使用 10 位數的金鑰
        current_key = key[i % len(key)]
        
        decrypted_char_code = 0
        if current_key == 1:
            decrypted_char_code = word ^ 0xad
        elif current_key == 2:
            decrypted_char_code = (word ^ 0xb2) + 1
        elif current_key == 3:
            decrypted_char_code = word ^ 0x57
        elif current_key == 4:
            decrypted_char_code = (word ^ 0x49) + 3
        elif current_key == 5:
            decrypted_char_code = word ^ 0x46
        elif current_key == 6:
            decrypted_char_code = (word ^ 0x57) - 2
        
        # 將解密後的 ASCII 碼轉換為字元，並拼接到最終結果中
        decrypted_flag += chr(decrypted_char_code & 0xFF)

    return decrypted_flag

# 執行解密並印出結果
if __name__ == "__main__":
    flag = decrypt_flag()
    print("解密後的 FLAG 是：")
    print(flag)
```

蠻有趣的題目
