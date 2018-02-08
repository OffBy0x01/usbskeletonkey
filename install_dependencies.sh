#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install rpi-update python git python-dev  python-pip sqlite3 isc-dhcp-server python-crypto inotify-tools screen

if ! sudo uname -a | grep -q "4.4.50+"; then
	sudo BRANCH=master rpi-update 5224108
	sudo reboot now	
fi

sudo touch /boot/ssh

if sudo grep -q "usb0" /etc/network/interfaces; then
	echo "usb0 already configured"
else
	cat /home/pi/usbskeletonkey/config/usb0-config | sudo tee --append /etc/network/interfaces > /dev/null
fi

if sudo grep -q "dtoverlay=dwc2" /boot/config.txt; then
	echo "dwc2 Already enabled"
else
	echo "dtoverlay=dwc2" | sudo tee --append /boot/config.txt > /dev/null
fi
if sudo grep -q "dwc2" /etc/modules; then
	echo "Modules already set"
else
	echo "dwc2" | sudo tee --append /etc/modules > /dev/null
fi

sudo bash <(curl -S https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv6l.sh)

echo "run this:"
echo "./conda config --add channels rpi"
echo "./conda install python=3.6"

