#!/bin/bash

rm -rf ./rootfs && mkdir rootfs
pushd . && pushd rootfs
cp ../rootfs.cpio.gz .
gzip -dc rootfs.cpio.gz | cpio -idm &>/dev/null
rm rootfs.cpio.gz
popd

