#!/bin/bash

qemu-system-x86_64 \
  -m 2G \
  -smp 2 \
  -nographic \
  -drive file=ubuntu-24.04-minimal-cloudimg-amd64.img,format=qcow2,if=virtio \
  -drive file=cloudinit.iso,format=raw,if=virtio \
  -net nic -net user,hostfwd=tcp::2222-:22
