#!/bin/bash

PF=printflag
PF_ENC=$(base64 -w 0 "$PF")

SETUP=setup.sh
SETUP_ENC=$(base64 -w 0 "$SETUP")

ROOT_PWD="xjAH3gjRbYhhAsbK"

cat <<EOF > meta-data
instance-id: greyhats-server
local-hostname: greyhats-server
EOF

cat <<EOF > user-data
#cloud-config
disable_root: false
ssh_pwauth: true
chpasswd:
  list: |
    root:$ROOT_PWD
  expire: false
hostname: greyhats-server
write_files:
  - path: /printflag
    encoding: b64
    permissions: '0710'
    content: |
      $PF_ENC
  - path: /root/setup.sh
    encoding: b64
    permissions: '0700'
    content: |
      $SETUP_ENC
EOF

cloud-localds cloudinit.iso user-data meta-data
