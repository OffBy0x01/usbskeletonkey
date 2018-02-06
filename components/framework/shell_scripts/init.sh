#!/usr/bin/env bash
cp ../../dhcpd.conf /etc/dhcp/dhcpd.conf  # Copy DHCP configs
# Do the same for /etc/dhcpcd.conf and /etc/network/interfaces
/etc/init.d/isc-dhcp-server stop  # Ensure DHCP server is stopped
