#!/usr/bin/env bash

# Function to convert netmask to CODR notation
# Source:
# https://www.linuxquestions.org/questions/programming-9/bash-cidr-calculator-646701/
mask2cidr() {
    nbits=0
    IFS=.
    for dec in $1 ; do
        case $dec in
            255) let nbits+=8;;
            254) let nbits+=7;;
            252) let nbits+=6;;
            248) let nbits+=5;;
            240) let nbits+=4;;
            224) let nbits+=3;;
            192) let nbits+=2;;
            128) let nbits+=1;;
            0);;
            *) echo "Error: $dec is not recognised"; exit 1
        esac
    done
    echo "$nbits"
}

# Print existing config
cat /etc/network/interfaces
# Ask user if config is to be kept
read -p "Edit current network configuration (Y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Ensure DHCP server is stopped
    /etc/init.d/isc-dhcp-server stop

    # Get source dir
    srcdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    # Copy default network configs
    cp $srcdir../../../config/interfaces /etc/network/interfaces  # Set interfaces for usb0
    cp $srcdir../../../config/dhcpcd.conf /etc/dhcpcd.conf  # Set static IPs for wlan0 and usb0
    cp $srcdir../../../config/resolv.conf /etc/resolv.conf  # Set DNS server
    cp $srcdir../../../config/dhcpd.conf /etc/dhcp/dhcpd.conf  # Set subnet for the DHCP server
    cp $srcdir../../../config/isc-dhcp-server /etc/default/isc-dhcp-server  # Set interface for DHCP server

    # Prompt user for config
    echo "Config wlan0"
    read -p "Enter IP address for device: " _address
    read -p "Enter netmask: " _netmask
    read -p "Enter network address: " _network
    read -p "Enter broadcast address: " _broadcast
    read -p "Enter network gateway: " _gateway
    read -p "Enter SSID: " _ssid
    read -p "Enter Passkey: " _psk

    # Convert netmask into CIDR notation
    _CIDRmask=$(mask2cidr $_netmask)

    # Apply config
    # Interfaces
    _interfaces=/etc/network/interfaces # File path
    sed -i -r "1,16{s,address .*,address $_address,g}" $_interfaces
    sed -i -r "1,16{s,netmask .*,netmask $_netmask,g}" $_interfaces
    sed -i -r "1,16{s,network .*,network $_network,g}" $_interfaces
    sed -i -r "1,16{s,broadcast .*,broadcast $_broadcast,g}" $_interfaces
    sed -i -r "1,16{s,gateway .*,gateway $_gateway,g}" $_interfaces
    sed -i -r "1,16{s,wpa-ssid .*,wpa-ssid \"$_ssid\",g}" $_interfaces
    sed -i -r "1,16{s,wpa-psk .*,wpa-psk \"$_psk\",g}" $_interfaces

    # dhcpcd.conf
    _dhcpcd=/etc/dhcpcd.conf # File path
    sed -i -r "62,62{s,static ip_address=.*,static ip_address=$_address\/$_CIDRmask,g}" $_dhcpcd

    # Down and up adapter for new config to take effect
    ip addr flush dev wlan0
    ifdown wlan0
    ifup wlan0
    ifconfig wlan0 up

    # Test for connection
    wget -q --tries=10 --timeout=20 --spider http://google.com
    if [[ $? -eq 0 ]]; then
            echo "Connection Successful!"
    else
            echo "Error connecting to internet - check configuration!"
    fi
else
    exit 1
fi
