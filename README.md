# Bus Spider
flexible open source hacker multi-tool

```diff
- Тут description
- Bus Spider uses protocol for Bus Pirate!
```

This repo contains source codes for Bus Spider hardware and software.

   * [running from pre-build images](#running-from-pre-build-images)
      * [требования для burning images on sd-card &amp; running minicom](#требования-для-burning-images-on-sd-card--running-minicom)
      * [how to burn images on(?) SD-card](#how-to-burn-images-on-sd-card)
      * [how to turn DE10-Nano On, boot Debian Linux and check 'minicom AL1'](#how-to-turn-de10-nano-on-boot-debian-linux-and-check-minicom-al1)
      * [how to add UEXT connector to DE10-Nano (cross-board schematics and UEXT pinout)](#how-to-add-uext-connector-to-de10-nano-cross-board-schematics-and-uext-pinout)
      * [how to examine I2C device (demo)](#how-to-examine-i2c-device-demo)
   * [Full rebuild](#full-rebuild)
      * [Prerequisites](#prerequisites)
         * [Install Quartus-lite 17.1](#install-quartus-lite-171)
         * [Install sudo](#install-sudo)
         * [Install necessary Debian Packages](#install-necessary-debian-packages)
      * [Собственно пересборка](#Собственно-пересборка)
         * [Сборка U-Boot](#Сборка-u-boot)
         * [Сборка ядра linux](#Сборка-ядра-linux)
         * [Сборка Debian ARM rootfs](#Сборка-debian-arm-rootfs)
         * [RISC-V QEMU](#risc-v-qemu)
         * [RISC-V toolchain](#risc-v-toolchain)
         * [nmon: RISC-V bootrom software](#nmon-risc-v-bootrom-software)
         * [FPGA bitstream for DE10-Nano](#fpga-bitstream-for-de10-nano)
         * [Bus Spider RISC-V firmware](#bus-spider-risc-v-firmware)
   * [NFS](#nfs)
      * [TODO: Настройка U-boot при первом включении](#todo-Настройка-u-boot-при-первом-включении)
         * [Настрока сети в U-Boot](#Настрока-сети-в-u-boot)
         * [Настройка tftp-сервера](#Настройка-tftp-сервера)
   * [Links](#links)


```diff
- Один параграф:
-    1. running Bus Spider on DE10-Nano from prebuild images
-    2. длинный процесс генерации всех images from sources
-    3. Bus Spider development from NFS-server
```

## running from pre-build images

### требования для burning images on sd-card & running minicom
Должен быть Linux box (e.g. Debian).

Нужны tar & dd и декомпрессор (xz --- apt-get install xz-utils) для burning U-Boot.

Нужны fdisk, e2fsprogs и dosfstools.

Нужен minicom (или screen или picocom). Можно сослаться на готовое руководство по смотрению в UART
DE1-SoC/DE10-Nano и пр.

```
  * u-boot-with-spl.sfp              --- U-Boot bootloader image

  * de10-nano-bus-spider_0.rbf       --- FPGA bitstream

  * zImage                           --- ARM Linux kernel image
  * socfpga_cyclone5_de10_nano.dtb   --- device tree blob for ARM Linux kernel

  * debian-stretch-armhf.tar.gz      --- ARM Linux rootfs

  * bus_spider.nmon                  --- RISC-V SoC firmware
```

```diff
- FIXME: use xz instead of gz
```

### how to burn images on(?) SD-card

```diff
- FIXME: TODO: скрипт разметки
scripts/mk-sd-card-parts.sh /dev/sdX
```


В результате работы скрипта на SD-карте должны получиться следующие разделы:

```
+---+------+-----+-----------+
| N | Size | Id  |   Type    |
+===+======+=====+===========+
| 1 |  8M  | a2  | unknown   |
+---+------+-----+-----------+
| 2 | 128M |  b  | W95 FAT32 |
+---+------+-----+-----------+
| 3 | ---- | 83  | Linux     |
+===+======+=====+===========+
```

В разделе 1 (ID=0xa2) хранится U-Boot.

Раздел с загрузчиком обязательно должен иметь ID=0xa2!

Раздел 2 (ID=0x0b) предназначен для хранения образа ядра Linux, файлов device tree и файлов битовых потоков ПЛИС. Указанные файлы будут использованы U-Boot при загрузке.

Раздел 3 (ID=0x83) предназначен для хранения корневой файловой системы Linux.



```
dd if=u-boot-with-spl.sfp of=/dev/sdX1
```

```diff
-tar -C $MOUNTPOINT vfx debian-stretch-armhf.tar.xz
```

Add AL0 and AL1 minicom configurations with Ctrl-B escape-key.

```
MOUNTPOINT=/mnt
mount /dev/sdX3 $MOUNTPOINT
tar -C $MOUNTPOINT vfx debian-stretch-armhf.tar.gz

mkdir -p $MOUNTPOINT/etc/minicom

cat <<EOF > $MOUNTPOINT/etc/minicom/minirc.AL0
pu port             /dev/ttyAL0
pu baudrate         115200
pu bits             8
pu parity           N
pu stopbits         1
pu escape-key       ^B
pu rtscts           No
EOF

cat <<EOF > $MOUNTPOINT/etc/minicom/minirc.AL1
pu port             /dev/ttyAL1
pu baudrate         115200
pu bits             8
pu parity           N
pu stopbits         1
pu escape-key       ^B
pu rtscts           No
EOF
```


### how to turn DE10-Nano On, boot Debian Linux and check 'minicom AL1'

```diff
- FIXME: ссылка на User Manual.
```

* подключите UART;
* подключите питание;


### how to add UEXT connector to DE10-Nano (cross-board schematics and UEXT pinout)

```diff
- FIXME: добавить картинку-schematic
```
```diff
- FIXME: Добавить предложение вида --- проверяйте по SDC.
```


### how to examine I2C device (demo)

See https://www.youtube.com/watch?v=xk4pjrGDSXQ#t=4m15s

```
[ 0x70 0xc8 0xf0 0xe0 0x08 0xd0 0xd4 ] -> 9
[ 0x70 0xc8 0xf0 0xe0 0x0c 0xd0 0xd4 ] -> 9
[ 0x70 0xc8 0xf0 0xe0 0x10 0x90 0x96 ] -> 0
[ 0x70 0xc8 0xf0 0xe0 0x14 0x91 0x07 ] -> M
[ 0x70 0xc8 0xf0 0xe0 0x18 0x40 0xd6 ] -> E
[ 0x70 0xc8 0xf0 0xe0 0x1c 0x00 0x00 ]
[ 0x70 0xc8 0xf0 0xe0 0x20 0x00 0x00 ]
[ 0x70 0xc8 0xf0 0xe0 0x00 0x00 0x00 ]
```

```diff
- тут фото
```


## Full rebuild

```diff
- Один параграф: что тут будет происходить длинный процесс генерации
```


### Prerequisites
Please use Debian 9 "Stretch". See https://www.debian.org for details.

You can use minimal Debian 9 x86_64 with ssh-server.
Your Install 4 GB of RAM for Quartus. Otherwise you will get a message like this from Quartus:

```
Out of memory in module quartus_map (3085 megabytes used)
Makefile:10: recipe for target 'map' failed
```


#### Install Quartus-lite 17.1

Install Quartus Prime Lite Edition 17.1.0.


#### Install sudo
The 'sudo' command is used in this manual. Install it. Login as root and run

```
apt-get install -y sudo
```

You may want to execute sudo without password. Follow these links to select appropriate solution:

  * https://askubuntu.com/questions/147241/execute-sudo-without-password
  * https://askubuntu.com/a/368230
  * http://jeromejaglale.com/doc/unix/ubuntu_sudo_without_password


#### Install necessary Debian Packages

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

Install packages for ARM Debian rootfs regeneration
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


### Собственно пересборка
#### Сборка U-Boot

```
make -s -C u-boot ARCH=arm socfpga_de10_nano_defconfig
make -s -C u-boot ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp u-boot/u-boot-with-spl.sfp $OUTPUT
```

```diff
-При сборке u-boot будет сделана утилита
-./u-boot/tools/mkimage
-которую приходится использовать для компиляции скриптов u-boot.
-Альтернативно можно поставить пакет Debian u-boot-tools
```


#### Сборка ядра linux

```
make -s -C linux ARCH=arm socfpga_de10_nano_defconfig
make -s -C linux ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-

cp linux/arch/arm/boot/zImage $OUTPUT
cp linux/arch/arm/boot/dts/socfpga_cyclone5_de10_nano.dtb $OUTPUT
```

#### Сборка Debian ARM rootfs

```
( cd output && sudo ../scripts/mk-debian-rootfs.sh )
```


#### RISC-V QEMU

```
( cd riscv-qemu && ./configure --target-list=riscv32-softmmu,riscv64-softmmu --prefix=/opt/riscv )
make -C riscv-qemu install
```


#### RISC-V toolchain

```
( cd riscv-gnu-toolchain && ./configure --prefix=/opt/riscv --with-arch=rv32i )
( make -C riscv-gnu-toolchain newlib )
```


#### nmon: RISC-V bootrom software

This step is not necessary. riscv-soc-cores already contains pre-compiled stable nmon image. This step demonstrate how to change nmon.

```
make -s -C riscv-nmon CROSS_COMPILE=/opt/riscv/bin/riscv32-unknown-elf- nmon_picorv32-wb-soc_24MHz_115200.txt
```


#### FPGA bitstream for DE10-Nano

```
( QP=/opt/altera/17.1/quartus && export PATH=$PATH:$QP/sopc_builder/bin:$QP/bin && \
  cd riscv-soc-cores && fusesoc --cores cores/ build de10-nano-bus-spider )

cp riscv-soc-cores/build/de10-nano-bus-spider_0/bld-quartus/de10-nano-bus-spider_0.rbf $OUTPUT
```


#### Bus Spider RISC-V firmware

```
make -s -C bus-spider-firmware CROSS_COMPILE=/opt/riscv/bin/riscv32-unknown-elf- bus_spider.nmon
cp bus-spider-firmware/bus_spider.nmon $OUTPUT
```

## NFS
### TODO: Настройка U-boot при первом включении

#### Настрока сети в U-Boot

При первом старте U-Boot выдаёт сообщение об ошибке контроллера Ethernet:

```
Loading Environment from MMC... *** Warning - bad CRC, using default environment

Failed (-5)
In:    serial
Out:   serial
Err:   serial
Model: Terasic DE10-Nano
Net:
Error: ethernet@ff702000 address not set.
No ethernet found.
Hit any key to stop autoboot:  0
=>
```

При этом заставить U-boot выполнять обмены по Ethernet не получится.

Дело в том, что для контроллера Ethernet не установлен MAC-адрес.

Установить MAC-адрес и записать его в хранилище на SD-карте можно так:

```
=> setenv ethaddr 00:01:02:03:04:05
=> saveenv
Saving Environment to MMC... Writing to MMC(0)... OK
=>
```

После следующей перезагрузки контроллер Ethernet станет доступен.

Отмечу, что хранилище параметров U-Boot находится на SD-карте за пределами разделов, а значит при форматировании разделов хранилище не будет затронуто.


#### Настройка tftp-сервера

Установить tftp-сервер:

```
sudo apt-get install -y tftpd-hpa
```

Для tftp-сервера необходимо задать каталог файловой системы, файлы из которого
доступны для загрузки по tftp.

В Debian за это отвечает переменная TFTP_DIRECTORY в файле /etc/default/tftpd-hpa.
По умолчанию в Debian TFTP_DIRECTORY="/srv/tftp". Также имеется практика использования
каталога /tftpboot. Для сохранения совместимости с этой практикой, а также для облегчения интеграции с NFS-сервером рекомендуется создать ссылку /tftpboot:

```
( cd / && sudo ln -s srv/tftp tftpboot )
```

#### Настройка nfs-сервера



## Links

* [InnovateFPGA 2018 | EM099 | Bus Spider (Project Video)](https://www.youtube.com/watch?v=xk4pjrGDSXQ)
* [SparkFun's Bus Pirate v3.6a Hookup Guide](https://learn.sparkfun.com/tutorials/bus-pirate-v36a-hookup-guide)
* http://dangerousprototypes.com/docs/Bus_Pirate
* https://github.com/sparkfun/Bus_Pirate
* https://github.com/BusPirate/Bus_Pirate
* https://www.seeedstudio.com/Bus-Pirate-v3.6-universal-serial-interface-p-609.html

* Bus Pirate week
  * [Bus Pirate week day 1 - development](https://www.youtube.com/watch?v=VVyCg_JFt1E)
  * [Bus Pirate week, day 2 - accessories and cables](https://www.youtube.com/watch?v=kXOe5alq-as)
  * [Bus Pirate week, day 3 - cases](https://www.youtube.com/watch?v=Y7A0xOZJsoo)
  * [Bus Pirate week, day 5 - hack the Bus Pirate to measure capacitors](https://www.youtube.com/watch?v=SqPlSPK4zyo)
