#! /bin/sh

# Note: -serial mon:stdio is here for convenience purposes.
# Remotely the chal is run with -serial stdio.

qemu-system-x86_64 \
  -no-reboot \
  -cpu max \
  -net none \
  -serial mon:stdio \
  -display none \
  -monitor none \
  -vga none \
  -kernel bzImage \
  -initrd initrd.cpio.gz \
  -append "console=ttyS0" \
