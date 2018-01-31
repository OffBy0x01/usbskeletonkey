#!/usr/bin/env bash

/etc/init.d/isc-dhcp-server stop  # Stop DHCP server
ifconfig usb0 down  # USB networking down
ifdown usb0  # Down USB interface