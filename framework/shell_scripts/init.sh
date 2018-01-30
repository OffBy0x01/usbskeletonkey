#!/usr/bin/env bash

cp ../../dhcpd.conf /etc/dhcp/dhcpd.conf  # Copy DHCP configs
echo -e 'iface usb0 inet static\naddress 10.10.10.10\nnetmask 128.0.0.0\ngateway 10.10.10.1' >> /etc/network/interfaces  # Set static IP