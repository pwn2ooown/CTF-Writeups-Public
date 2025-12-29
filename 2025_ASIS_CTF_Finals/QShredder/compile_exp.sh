#!/bin/bash

in=exp.c
out=exp
musl-gcc $in -static -o $out || exit 255
base64 -w 200 $out > ooo.bin
mv $out initramfs
pushd . && pushd initramfs
find . -print0 | cpio --null --format=newc -o 2>/dev/null | gzip -9 > ../initramfs.cpio.gz
popd