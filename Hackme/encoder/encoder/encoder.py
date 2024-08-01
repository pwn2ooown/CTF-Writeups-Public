#!/usr/bin/env python2

import random
import string

def rot13(s):
    return s.translate(string.maketrans(string.uppercase + string.lowercase,
        string.uppercase[13:] + string.uppercase[:13] +
        string.lowercase[13:] + string.lowercase[:13]))

def base64(s):
    return ''.join(s.encode('base64').split())

def hex(s):
    return s.encode('hex')

def upsidedown(s):
    return s.translate(string.maketrans(string.uppercase + string.lowercase,
        string.lowercase + string.uppercase))

flag = 'FLAG{.....................}'  # try to recover flag

E = (rot13, base64, hex, upsidedown)

for i in range(random.randint(30, 50)):
    print i
    c = random.randint(0, len(E) - 1)
    flag = '%d%s' % (c, E[c](flag))

open('flag.enc', 'w').write(flag)
