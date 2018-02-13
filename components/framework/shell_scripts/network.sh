#!/usr/bin/env bash

cp ../../../config/interfaces /etc/network/interfaces
cp ../../../config/dhcpcd.conf /etc/dhcpcd.conf
cp ../../../config/resolv.conf /etc/resolv.conf
cp ../../../config/dhcpd.conf /etc/dhcp/dhcpd.conf
cp ../../../config/isc-dhcp-server /etc/default/isc-dhcp-server

ifdown wlan0
ifup wlan0
ifconfig wlan0 up