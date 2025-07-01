# Setup instructions

1. Download cloud-minimal Ubuntu 24.04: `wget https://cloud-images.ubuntu.com/minimal/releases/noble/release/ubuntu-24.04-minimal-cloudimg-amd64.img`
2. Make a copy of the image for backup: `cp ubuntu-24.04-minimal-cloudimg-amd64.img ubuntu-24.04-minimal-cloudimg-amd64.img.bak` 
3. Run the build script to generate the cloudinit configuration for the image: `./build.sh`
4. Start the qemu emulator with the given image and cloudinit config: `./run-chal-qemu.sh`
5. After logging in to root in qemu, run `./setup.sh` in the /root folder to setup the vm
6. Done! (default port for ssh is 2222, change it in the qemu script if necessary)

## If you messed something up
1. Kill the VM: `Ctrl-A X`
2. Run the reset script to delete the qemu image and copy the backup version: `./reset.sh`

