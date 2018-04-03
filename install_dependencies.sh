#!/usr/bin/env bash
# MUST BE RUN AS ROOT!

# Network set up
./components/framework/shell_scripts/network_setup.sh

# Install Dependencies
apt-get update
apt-get --assume-yes install rpi-update
apt-get --assume-yes install python
apt-get --assume-yes install git
apt-get --assume-yes install python-dev
apt-get --assume-yes install python-pip
apt-get --assume-yes install sqlite3
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install python-crypto
apt-get --assume-yes install inotify-tools
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# TODO Comments
if ! uname -a | grep -q "4.4.50+"; then
	BRANCH=master rpi-update 5224108
	reboot now
fi

touch /boot/ssh

if grep -q "usb0" /etc/network/interfaces; then
	echo "usb0 already configured"
else
	cat /home/pi/usbskeletonkey/config/usb0-config | tee --append /etc/network/interfaces > /dev/null
fi

if grep -q "dtoverlay=dwc2" /boot/config.txt; then
	echo "dwc2 Already enabled"
else
	echo "dtoverlay=dwc2" | tee --append /boot/config.txt > /dev/null
fi
if grep -q "dwc2" /etc/modules; then
	echo "Modules already set"
else
	echo "dwc2" | tee --append /etc/modules > /dev/null
fi

mv /home/pi/usbskeletonkey/components/framework/shell_scripts/g_hid.ko /lib/modules/4.4.50+/kernel/drivers/usb/gadget/legacy/g_hid.ko
chmod +x /home/pi/usbskeletonkey/components/framework/shell_scripts/hid-gadget-test

# TODO Test this
# Install python 3.6
# ( cd ~ ;
# bash <(curl -S https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv6l.sh) ;
# ./conda config --add channels rpi ;
# ./conda install python=3.6)

sed -i -r "1,16{s,first_run .*,first_run = false,g}" ./config.ini
