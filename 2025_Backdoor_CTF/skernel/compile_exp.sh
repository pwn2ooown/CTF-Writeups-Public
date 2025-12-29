#!/bin/bash
in=exp.c
out=exp
python3 generate_shellcode.py
xxd -i shellcode > shellcode.h
gcc $in -static -o $out  || exit 255
