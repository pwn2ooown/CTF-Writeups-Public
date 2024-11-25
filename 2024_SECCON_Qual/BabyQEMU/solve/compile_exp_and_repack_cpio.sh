#!/bin/bash
gcc exp.c -static -o exp || exit 255 # Or use musl-gcc
mv exp rootfs
pushd . && pushd rootfs
find . -print0 | cpio --null --format=newc -R root -o 2>/dev/null | gzip -9 > ../rootfs.cpio.gz # -R root is needed
popd

