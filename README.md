# Bus Spider

The Bus Spider is open source network enabled electronic multi-tool for enthusiasts and professionals.<br/>
This project is heavily influenced and inspired by the Bus Pirate http://dangerousprototypes.com/docs/Bus_Pirate

The Bus Spider aims to implement Bus Pirate's protocol and preserve compatibility while providing more functions.<br/>
Network capabilities of the Bus Spider will allow to use it as core device for remote control and debug.

This repo contains source codes for Bus Spider hardware and software for implementation on the Terasic DE10-Nano development board.


## Table of contents

   * [Running Bus Spider from prebuilt images](#running-bus-spider-from-prebuilt-images)
   * [Building Bus Spider from scratch](#building-bus-spider-from-scratch)
      * [Prerequirements](#prerequirements)
      * [Clone Bus Spider repository and prepare it to build](#clone-bus-spider-repository-and-prepare-it-to-build)
      * [Install RISC-V GNU toolchain and QEMU from Bus Spider repository](#install-risc-v-gnu-toolchain-and-qemu-from-bus-spider-repository)
      * [Building U-Boot bootloader image](#building-u-boot-bootloader-image)
      * [Building FPGA bitstream](#building-fpga-bitstream)
      * [Building Linux kernel image for HPS](#building-linux-kernel-image-for-hps)
      * [Building Linux rootfs for HPS](#building-linux-rootfs-for-hps)
      * [Building Bus Spider RISC-V SoC firmware](#building-bus-spider-risc-v-soc-firmware)
      * [Burn images to SD-card](#burn-images-to-sd-card)
   * [Start Bus Spider](#start-bus-spider)
   * [Configuring Bus Spider to use NFS rootfs](#configuring-bus-spider-to-use-nfs-rootfs)
      * [TFTP-server setup](#tftp-server-setup)
      * [NFS-server setup](#nfs-server-setup)
      * [First run U-boot configuration](#first-run-u-boot-configuration)
      * [Using U-Boot scripts for running Linux with NFS rootfs](#using-u-boot-scripts-for-running-linux-with-nfs-rootfs)
      * [First run Linux configuration](#first-run-linux-configuration)
   * [Uploading Bus Spider SoC firmware from HPS hosted Linux](#uploading-bus-spider-soc-firmware-from-hps-hosted-linux)
   * [Accessing Bus Spider CLI from HPS hosted Linux](#accessing-bus-spider-cli-from-hps-hosted-linux)
   * [DE10-Nano base Bus Spider connectivity list](#de10-nano-base-bus-spider-connectivity-list)
   * [Work with Bus Spider](#work-with-bus-spider)
      * [I2C](#i2c)
      * [SPI](#spi)
   * [Resetting Bus Spider RISC-V SoC from HPS hosted Linux](#resetting-bus-spider-risc-v-soc-from-hps-hosted-linux)
   * [Links](#links)
      * [Bus Pirate](#bus-pirate)
         * [XC6BP – FPGA Based 'Bus Pirate'](#xc6bp--fpga-based-bus-pirate)


## Running Bus Spider from prebuilt images
**Pending**


## Building Bus Spider from scratch

### Prerequirements

This instruction is valid for Debian 9 "Stretch". See https://www.debian.org for details.
4GB of RAM is needed if you are running Quartus Prime software to build FPGA bitstream.
This instruction may work for **Ubuntu 16.04** but results are not guaranteed.

1. Make sure that basic utilities are available<br/>
output of these commands shouldn't be empty:
```
which tar
which dd
which sudo
which xz
```

2. Make sure that disk utilities are available<br/>
output of these commands shouldn't be empty:
```
which fdisk
which e2fsprogs
which dosfstools
```

3. Make sure that serial communication utilities are available:<br/>
output of this command shouldn't be empty:
```
which minicom
```
alternatively you can use `screen` or `picocom`


4. Make sure that `git` is available:<br/>
output of this command shouldn't be empty:
```
which git
```

5. Install ARM GNU toolchain for building HPS Linux kernel and U-Boot:
```
sudo apt-get install -y make gcc gawk bc libssl-dev
sudo apt-get install -y gcc-arm-linux-gnueabihf
```

6. Install packages for ARM Debian rootfs regeneration
```
sudo apt-get install -y binfmt-support qemu qemu-user-static debootstrap
```

7. Install `fusesoc` version **1.8.1**:
```
sudo apt-get install -y python3-pip
sudo pip3 install fusesoc==1.8.1
```

8. Install `Quartus Prime Lite` version **17.1**

We recommend install Quartus Prime Lite into ```/opt/altera/17.1``` directory.


9. Install packages required for riscv-gnu-toolchain & riscv-qemu build
```
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y texinfo bison flex libgmp-dev libmpfr-dev libmpc-dev
sudo apt-get install -y python pkg-config libglib2.0-dev libpixman-1-dev
```

10. Create global user-writable RISC-V tools install path
```
sudo mkdir -p /opt/riscv
sudo chown $USER /opt/riscv
```

### Clone Bus Spider repository and prepare it to build
```
git clone --recursive https://github.com/miet-riscv-workgroup/de10-nano-bus-spider
cd de10-nano-bus-spider
OUTPUT=output
mkdir -p $OUTPUT
```

### Install RISC-V GNU toolchain and QEMU from Bus Spider repository

1. Install RISC-V QEMU
```
( cd riscv-qemu && ./configure --target-list=riscv32-softmmu,riscv64-softmmu --prefix=/opt/riscv )
make -C riscv-qemu install
```

2. Install RISC-V GNU toolchain
```
( cd riscv-gnu-toolchain && ./configure --prefix=/opt/riscv --with-arch=rv32i )
( make -C riscv-gnu-toolchain newlib )
```

### Building U-Boot bootloader image
Result of this step is `u-boot-with-spl.sfp` --- U-Boot bootloader image
```
make -s -C u-boot ARCH=arm socfpga_de10_nano_defconfig
make -s -C u-boot ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp u-boot/u-boot-with-spl.sfp $OUTPUT
```

### Building FPGA bitstream
Result of this step is `de10-nano-bus-spider_0.rbf` --- Cyclone V SoC FPGA bitstream
```
( QP=/opt/altera/17.1/quartus && export PATH=$PATH:$QP/sopc_builder/bin:$QP/bin && \
  cd riscv-soc-cores && fusesoc --cores cores/ build de10-nano-bus-spider )

cp riscv-soc-cores/build/de10-nano-bus-spider_0/bld-quartus/de10-nano-bus-spider_0.rbf $OUTPUT
```

### Building Linux kernel image for HPS
Results of this step are:
  * `socfpga_cyclone5_de10_nano.dtb`   --- device tree blob for ARM Linux kernel
  * `zImage`                           --- ARM Linux kernel image
```
make -s -C linux ARCH=arm socfpga_de10_nano_defconfig
make -s -C linux ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp linux/arch/arm/boot/zImage $OUTPUT
cp linux/arch/arm/boot/dts/socfpga_cyclone5_de10_nano.dtb $OUTPUT
```

### Building Linux rootfs for HPS
Result of this step is `debian-stretch-armhf.tar.xz` --- ARM Linux rootfs
```
( cd output && sudo ../scripts/mk-debian-rootfs.sh )

```

### Building Bus Spider RISC-V SoC firmware
Result of this step is `bus_spider.nmon` --- RISC-V SoC firmware
```
make -s -C bus-spider-firmware CROSS_COMPILE=/opt/riscv/bin/riscv32-unknown-elf- bus_spider.nmon
cp bus-spider-firmware/bus_spider.nmon $OUTPUT
```

### Burn images to SD-card
Partition SD-card:<br/>
**Pending**

Check partition table on SD-card:<br/>
**Pending**

Output of this command should be:
```
+---+------+----+-----------+
| N | Size | Id |   Type    |
+===+======+====+===========+
| 1 |  8M  | a2 | unknown   |
+---+------+----+-----------+
| 2 | 128M | 0b | W95 FAT32 |
+---+------+----+-----------+
| 3 | ---- | 83 | Linux     |
+===+======+====+===========+
```

Partition 1 is for U-Boot. Double check it's ID=0xA2.<br/>
Partition 2 is for Linux kernel image, Device Tree files and FPGA bitstreams.<br/>
Partition 3 is for local Linux rootfs

```
dd if=u-boot-with-spl.sfp of=/dev/sdX1
```

## Start Bus Spider

1. Plug prepared SD-card in DE10-Nano SD-card slot
2. Connect DE10-Nano to the LAN using Ethernet cable
3. Connect DE10-Nano UART to the PC using miniUSB cable
4. Power up DE10-Nano


## Configuring Bus Spider to use NFS rootfs

### TFTP-server setup
**Pending**


### NFS-server setup
**Pending**


### First run U-boot configuration
**Pending**

```
=> setenv ethaddr 00:01:02:03:04:05
=> saveenv
Saving Environment to MMC... Writing to MMC(0)... OK
=>
```

### Using U-Boot scripts for running Linux with NFS rootfs
**Pending**

### First run Linux configuration
**Pending**

1. Use ssh to access Bus Spider Linux Host (HPS subsystem)
2. Add AL0 and AL1 minicom configurations:

```
mkdir -p /etc/minicom

cat <<EOF > /etc/minicom/minirc.AL0
pu port             /dev/ttyAL0
pu baudrate         115200
pu bits             8
pu parity           N
pu stopbits         1
pu escape-key       ^B
pu rtscts           No
EOF

cat <<EOF > /etc/minicom/minirc.AL1
pu port             /dev/ttyAL1
pu baudrate         115200
pu bits             8
pu parity           N
pu stopbits         1
pu escape-key       ^B
pu rtscts           No
EOF
```


## Uploading Bus Spider SoC firmware from HPS hosted Linux
**Pending**


## Accessing Bus Spider CLI from HPS hosted Linux
**Pending**


## DE10-Nano base Bus Spider connectivity list

```diff
- FIXME: add connectivity schematic
```
```diff
- FIXME: use Quartus sdc-files to check devboard-UEXT connectivity
```


## Work with Bus Spider

### I2C

* see [LCD1X9.md](doc/LCD1X9.md)
* see [TinyRTC.md](doc/TinyRTC.md)

### SPI

* see [Winbond-W25Q16.md](doc/Winbond-W25Q16.md)


## Resetting Bus Spider RISC-V SoC from HPS hosted Linux
```
GPIO=/sys/class/gpio; echo 2040 > $GPIO/export
echo high > $GPIO/gpio2040/direction; echo low > $GPIO/gpio2040/direction

# https://www.kernel.org/doc/Documentation/gpio/sysfs.txt
# GPIO=/sys/class/gpio
# echo 2040 > $GPIO/export
# echo 2047 > $GPIO/export
# echo high > $GPIO/gpio2040/direction
# echo high > $GPIO/gpio2047/direction
# echo low > $GPIO/gpio2040/direction
# echo low > $GPIO/gpio2047/direction
```


## Links

* [InnovateFPGA 2018 | EM099 | Bus Spider](http://www.innovatefpga.com/cgi-bin/innovate/teams.pl?Id=EM099)
* [InnovateFPGA 2018 | EM099 | Bus Spider (Project Video)](https://www.youtube.com/watch?v=xk4pjrGDSXQ)


### Bus Pirate

* http://dangerousprototypes.com/docs/Bus_Pirate
* [SparkFun's Bus Pirate v3.6a Hookup Guide](https://learn.sparkfun.com/tutorials/bus-pirate-v36a-hookup-guide)
* https://github.com/sparkfun/Bus_Pirate
* https://github.com/BusPirate/Bus_Pirate
* https://www.seeedstudio.com/Bus-Pirate-v3.6-universal-serial-interface-p-609.html

#### XC6BP – FPGA Based 'Bus Pirate' ####

* [XC6BP – FPGA Based 'Bus Pirate'](http://ultra-embedded.com/xc6bp-fpga-based-bus-pirate/)
* https://hackaday.com/2014/03/10/a-fpga-based-bus-pirate-clone/fpgapirate/
* http://robriglar.com/wordpress/wp-content/uploads/2014/03/fpga_xc6bp.tar.gz
