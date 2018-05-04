# Bus Spider
flexible open source hacker multi-tool

This repo contains source codes for Bus Spider hardware and software.


## Prerequisites
Please use Debian 9 "Stretch". See https://www.debian.org for details.

```
apt-get install gcc-arm-linux-gnueabihf

```


## U-Boot for DE10-Nano

From the de10-nano-bus-spider directory do the following:

```
OUTPUT=output
mkdir -p $OUTPUT

make -C u-boot ARCH=arm socfpga_de10_nano_defconfig
make -C u-boot -s ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp u-boot/spl/u-boot-spl.sfp $OUTPUT
cp u-boot/u-boot.img $OUTPUT
```


## Linux kernel for DE10-Nano

From the de10-nano-bus-spider directory do the following:

```
OUTPUT=output
mkdir -p $OUTPUT

make -C linux ARCH=arm socfpga_de10_nano_defconfig
make -C linux -s ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp linux/arch/arm/boot/zImage $OUTPUT
cp linux/arch/arm/boot/dts/socfpga_cyclone5_de10_nano.dtb $OUTPUT
```


## Links

* https://github.com/miet-riscv-workgroup/rv32-simple-soc
