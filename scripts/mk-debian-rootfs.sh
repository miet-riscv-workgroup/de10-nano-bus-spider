#!/bin/sh

set -e
set -x

ARCH=armhf

#
# https://wiki.debian.org/DebianStretch
# Stretch is the development codename for Debian 9.
#
DEBRELEASE=stretch

DEBMIRROR=http://ftp.us.debian.org/debian/
ROOTPASSWD="123"
#SUFFIX="-$(date +'%Y%m%d%H%M')"
SUFFIX=""

DEBROOTDIR=debian-${DEBRELEASE}-${ARCH}
#QEMUSTATIC=qemu-${ARCH}-static
QEMUSTATIC=qemu-arm-static

rm -rf $DEBROOTDIR

EXTRA_PACKAGES=openssh-server,net-tools,device-tree-compiler,minicom,i2c-tools,usbutils,lsscsi,less,expect,dosfstools

debootstrap --foreign --arch=${ARCH} \
		--include=${EXTRA_PACKAGES} \
		$DEBRELEASE $DEBROOTDIR $DEBMIRROR

cp /usr/bin/$QEMUSTATIC $DEBROOTDIR/usr/bin/

DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true \
        LC_ALL=C LANGUAGE=C LANG=C \
        PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin \
        chroot $DEBROOTDIR /debootstrap/debootstrap --second-stage

echo "root:$ROOTPASSWD" | chroot $DEBROOTDIR chpasswd

echo "${DEBRELEASE}" > $DEBROOTDIR/etc/hostname


#
# clean up
#
chroot $DEBROOTDIR apt-get clean
rm $DEBROOTDIR/usr/bin/$QEMUSTATIC

tar czf ${DEBROOTDIR}${SUFFIX}.tar.gz -C $DEBROOTDIR .
rm -rf $DEBROOTDIR
