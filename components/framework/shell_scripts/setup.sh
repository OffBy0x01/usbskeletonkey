#!/usr/bin/env bash
# MUST run as root!

# Install Requirements
apt-get update
# Ensure Python is installed
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# Network set up
# echo -e '\nallow-hotplug wlan0\niface wlan0 inet static\naddress 192.168.0.237\nnetmask 255.255.255.0\n\nallow-hotplug usb0\niface usb0 inet static\naddress 10.10.10.10\nnetmask 128.0.0.0\ngateway 10.10.10.1' >> /etc/network/interfaces  # Set static IP in interfaces
# echo -e '\ninterface wlan0\nstatic ip_address=192.168.0.237/24\n\ninterface usb0\nstatic ip_address=10.10.10.10/7' >> /etc/dhcpcd.conf # Set static IP in dhcpcd.conf

cp ../../../config/interfaces /etc/network/interfaces
cp ../../../config/dhcpcd.conf /etc/dhcpcd.conf
cp ../../../config/resolv.conf /etc/resolv.conf
ifdown wlan0
ifup wlan0
ifconfig wlan0 up

# compgen -c | grep "mkfs\."