# Bus Spider
flexible open source hacker multi-tool

This repo contains source codes for Bus Spider hardware and software.


## Prerequisites
Please use Debian 9 "Stretch" for 64-bit Intel and AMD CPU.
See https://www.debian.org for details.

You can use minimal Debian 9 x86_64 with ssh-server.
Your have to install at least 4 GB of RAM for running Quartus. Otherwise you will get a message like this from Quartus:

```
Out of memory in module quartus_map (3085 megabytes used)
Makefile:10: recipe for target 'map' failed
```


### Install Quartus-lite 17.1

Install Quartus Prime Lite Edition 17.1.0 in ```/opt/altera/17.1```.
See https://www.altera.com/products/design-software/fpga-design/quartus-prime/download.html for details.


#### Install sudo
The 'sudo' command is used in this manual. Install it. Login as root and run

```
apt-get install -y sudo
```

You may want to execute sudo without password. Follow these links to select appropriate solution:

  * https://askubuntu.com/questions/147241/execute-sudo-without-password
  * https://askubuntu.com/a/368230
  * http://jeromejaglale.com/doc/unix/ubuntu_sudo_without_password


### Install necessary Debian Packages

```
sudo apt-get install -y git
```

Install tools for ARM Linux kernel & U-Boot build:
```
sudo apt-get install -y make gcc gawk bc libssl-dev
sudo apt-get install -y gcc-arm-linux-gnueabihf
```

Install stable fusesoc
```
sudo apt-get install -y python3-pip
sudo pip3 install fusesoc==1.8.1
```

Install packages for riscv-gnu-toolchain & riscv-qemu build
```
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y texinfo bison flex libgmp-dev libmpfr-dev libmpc-dev
sudo apt-get install -y python pkg-config libglib2.0-dev libpixman-1-dev
```

Install packages for ARM Debian rootfs generation
```
sudo apt-get install -y binfmt-support qemu qemu-user-static debootstrap
```

Create global user-writable RISC-V tools install path

```
sudo mkdir -p /opt/riscv
sudo chown $USER /opt/riscv
```

This repository uses submodules. You need the ```--recursive``` option to fetch the submodules automatically

```
git clone --recursive https://github.com/miet-riscv-workgroup/de10-nano-bus-spider

cd de10-nano-bus-spider
```

Prepare directory for output files.
```
OUTPUT=output
mkdir -p $OUTPUT
```

## U-Boot for DE10-Nano

From the de10-nano-bus-spider directory do the following:

```
make -s -C u-boot ARCH=arm socfpga_de10_nano_defconfig
make -s -C u-boot ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp u-boot/u-boot-with-spl.sfp $OUTPUT
```


## Linux kernel for DE10-Nano

From the de10-nano-bus-spider directory do the following:

```
make -s -C linux ARCH=arm socfpga_de10_nano_defconfig
make -s -C linux ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp linux/arch/arm/boot/zImage $OUTPUT
cp linux/arch/arm/boot/dts/socfpga_cyclone5_de10_nano.dtb $OUTPUT
```

#### Debian ARM rootfs

From the de10-nano-bus-spider directory do the following:

```
( cd output && sudo ../scripts/mk-debian-rootfs.sh )
```


## FPGA bitstream for DE10-Nano

From the de10-nano-bus-spider directory do the following:

```
( QP=/opt/altera/17.1/quartus && export PATH=$PATH:$QP/sopc_builder/bin:$QP/bin && \
  cd riscv-soc-cores && fusesoc --cores cores/ build de10-nano-bus-spider )

cp riscv-soc-cores/build/de10-nano-bus-spider_0/bld-quartus/de10-nano-bus-spider_0.rbf $OUTPUT
```


## RISC-V QEMU

From the de10-nano-bus-spider directory do the following:

```
( cd riscv-qemu && ./configure --target-list=riscv32-softmmu,riscv64-softmmu --prefix=/opt/riscv && make install )
```


## RISC-V toolchain

From the de10-nano-bus-spider directory do the following:

```
( cd riscv-gnu-toolchain && ./configure --prefix=/opt/riscv --with-arch=rv32i && make newlib )
```


## nmon: RISC-V bootrom software

From the de10-nano-bus-spider directory do the following:

```
make -C riscv-nmon CROSS_COMPILE=/opt/riscv/bin/riscv32-unknown-elf- nmon_picorv32-wb-soc_24MHz_115200.txt
```


## Bus Spider RISC-V firmware

From the de10-nano-bus-spider directory do the following:

```
make -C bus-spider-firmware CROSS_COMPILE=/opt/riscv/bin/riscv32-unknown-elf-
cp bus-spider-firmware/bus_spider.bin $OUTPUT
```


## Links

* https://github.com/miet-riscv-workgroup/rv32-simple-soc
