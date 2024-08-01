from pwn import *

# Define input list
input_list = [4, 54, 41, 0, 112, 32, 25, 49, 33, 3, 0, 0, 57, 32, 108, 23, 48, 4, 9, 70, 7, 110, 36, 8, 108, 7, 49, 10, 4, 86, 43, 106, 123, 89, 87, 18, 62, 47, 10, 78]

# key_str = 'J_o3t'
key_str = b">\x00%\\G"
# Define key_list


# Print or use result_text
print(xor(xor(bytes(input_list),key_str),b"J_o3t").decode())

