#!/bin/bash

# Decompress a .cpio.gz packed file system
rm -rf ./initramfs && mkdir initramfs
pushd . && pushd initramfs
cp ../initramfs.cpio.gz .
gzip -dc initramfs.cpio.gz | cpio -idm &>/dev/null && rm initramfs.cpio.gz
popd
