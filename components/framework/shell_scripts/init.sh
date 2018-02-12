#!/usr/bin/env bash

/etc/init.d/isc-dhcp-server stop  # Ensure DHCP server is stopped

cp ../../../config/dhcpd.conf /etc/dhcp/dhcpd.conf  # Copy DHCP configs
cp ../../../config/dhcpcd.conf /etc/dhcpcd.conf
cp ../../../config/interfaces /etc/network/interfaces  # Copy interfaces