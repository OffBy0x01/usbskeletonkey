#!/usr/bin/env bash
# MUST run as root!

# Install Requirements
apt-get update
apt-get --assume-yes install python 3.6 # Ensure Python is installed
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# Make Files
# dhcpd.conf
mkdir -p /etc/dhcp
echo -e "# /etc/dhcp/dhcpd.conf \n # Needs Created" >> /etc/dhcp/dhcpd.conf

# compgen -c | grep "mkfs\."