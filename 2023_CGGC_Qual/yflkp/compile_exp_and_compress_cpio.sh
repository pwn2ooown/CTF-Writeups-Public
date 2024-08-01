#!/bin/bash

# Compress initramfs with the included statically linked exploit
in=$1
out=$(echo $in | awk '{ print substr( $0, 1, length($0)-2 ) }')
gcc $in -static -o $out || exit 255 # Or use musl-gcc
mv $out initramfs
pushd . && pushd initramfs
find . -print0 | cpio --null --format=newc -o 2>/dev/null | gzip -9 > ../initramfs.cpio.gz
popd
