#!/usr/bin/env bash

# Ensure DHCP server is stopped
/etc/init.d/isc-dhcp-server stop

# Copy network configs
cp ../../../config/interfaces /etc/network/interfaces  # Set interfaces for usb0
cp ../../../config/dhcpcd.conf /etc/dhcpcd.conf  # Set static IPs for wlan0 and usb0
cp ../../../config/resolv.conf /etc/resolv.conf  # Set DNS server
cp ../../../config/dhcpd.conf /etc/dhcp/dhcpd.conf  # Set subnet for the DHCP server
cp ../../../config/isc-dhcp-server /etc/default/isc-dhcp-server  # Set interface for DHCP server