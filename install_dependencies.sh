#!/usr/bin/env bash
# MUST BE RUN AS ROOT!

# Network set up

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
read -p "Keep current network configuration (Y/N): " -n 1 -r
echo
if ! [[ $REPLY =~ ^[Yy]$ ]]
then
    # Ensure DHCP server is stopped
    /etc/init.d/isc-dhcp-server stop

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
fi


# Test for connection
wget -q --tries=10 --timeout=20 --spider http://google.com
if [[ $? -eq 0 ]]; then
        echo "Connection Successful!"
else
        echo "Error connecting to internet - check configuration!"
        exit 0
fi

# Install Dependencies
apt-get update
apt-get --assume-yes install rpi-update
apt-get --assume-yes install python
apt-get --assume-yes install git
apt-get --assume-yes install python-dev
apt-get --assume-yes install python-pip
apt-get --assume-yes install sqlite3
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install python-crypto
apt-get --assume-yes install inotify-tools
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# Get required kernel version
if ! uname -a | grep -q "4.4.50+"; then
	BRANCH=master rpi-update 5224108
	reboot now
fi

# Enable SSH
touch /boot/ssh

# Check if usb0 is configured
if grep -q "usb0" /etc/network/interfaces; then
	echo "usb0 already configured"
else
	cat /home/pi/usbskeletonkey/config/usb0-config | tee --append /etc/network/interfaces > /dev/null
fi

# Check if dwc2 is enabled
if grep -q "dtoverlay=dwc2" /boot/config.txt; then
	echo "dwc2 Already enabled"
else
	echo "dtoverlay=dwc2" | tee --append /boot/config.txt > /dev/null
fi
if grep -q "dwc2" /etc/modules; then
	echo "Modules already set"
else
	echo "dwc2" | tee --append /etc/modules > /dev/null
fi

# Required for keyboard framework component
mv /home/pi/usbskeletonkey/components/framework/shell_scripts/g_hid.ko /lib/modules/4.4.50+/kernel/drivers/usb/gadget/legacy/g_hid.ko
chmod +x /home/pi/usbskeletonkey/components/framework/shell_scripts/hid-gadget-test

# sed -i -r "1,16{s,first_run .*,first_run = false,g}" ./config.ini
