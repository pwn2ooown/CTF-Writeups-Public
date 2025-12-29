#!/bin/bash
qemu-system-x86_64 \
    -m 128M \
    -kernel bzImage \
    -initrd initramfs.cpio \
    -append "console=ttyS0 kaslr loglevel=3 oops=panic panic=1 nopti quiet" \
    -cpu qemu64,+smep,+smap \
    -monitor /dev/null \
    -nographic \
    -no-reboot \
    -nic user,model=virtio\
    -smp 2
