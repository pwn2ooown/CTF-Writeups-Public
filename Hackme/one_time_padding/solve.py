#!/usr/bin/env python3
'''
We know that the key of opt has no null byte, so each byte of the cipher is "not" the original byte.
'''

import requests

url = 'https://ctf.hackme.quest/otp/?issue_otp=ooo'

def get_otp():
    r = requests.get(url)
    return r.text

FLAG_LEN = 50



# TODO: If assert failed, try brute force that byte again
# TODO: And maybe multithreading?
def main():
    leaked = "FLAG{"
    # otp = get_otp().split('\n')[:-1]
    # print(otp)
    for i in range(len(leaked),FLAG_LEN):
        print("Finding flag[{}]".format(i))
        ascii_table = [False] * 256
        for j in range(100):
            otp = get_otp().split('\n')[:-1]
            for o in otp:
                ooo = int(o[i*2:i*2+2],16)
                # print(ooo)
                ascii_table[ooo] = True
        # assert only one value is False
        # print(sum(ascii_table))
        assert sum(ascii_table) == 255
        for j in range(256):
            if not ascii_table[j]:
                leaked += chr(j)
                print("Found",chr(j))
                print("Flag now:",leaked)
                break


if __name__ == '__main__':
    main()