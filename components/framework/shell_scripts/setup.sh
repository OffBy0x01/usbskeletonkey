#!/usr/bin/env bash
# MUST run as root!

# Install Requirements
apt-get update
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# Network set up
cp ../../../config/interfaces /etc/network/interfaces  # Set interfaces for usb0
cp ../../../config/dhcpcd.conf /etc/dhcpcd.conf  # Set static IPs for wlan0 and usb0
cp ../../../config/resolv.conf /etc/resolv.conf  # Set DNS server
cp ../../../config/dhcpd.conf /etc/dhcp/dhcpd.conf  # Set subnet for the DHCP server
cp ../../../config/isc-dhcp-server /etc/default/isc-dhcp-server  # Set interface for DHCP server

# Down and up adapter for new config to take effect
ifdown wlan0
ifup wlan0
ifconfig wlan0 up

# compgen -c | grep "mkfs\."