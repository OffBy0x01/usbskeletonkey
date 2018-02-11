#!/usr/bin/env bash

/etc/init.d/isc-dhcp-server stop  # Ensure DHCP server is stopped

cp ../../../configs/dhcpd.conf /etc/dhcp/dhcpd.conf  # Copy DHCP configs
cp ../../../configs/dhcpcd.conf /etc/dhcpcd.conf
cp ../../../configs/interfaces /etc/network/interfaces  # Copy interfaces