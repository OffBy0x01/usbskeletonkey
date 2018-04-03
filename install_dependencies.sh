#!/usr/bin/env bash
# MUST BE RUN AS ROOT!

# Network set up

# Function calculates number of bit in a netmask
# Source from post 2
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

# Ensure DHCP server is stopped
/etc/init.d/isc-dhcp-server stop

# Copy default network configs
cp config/interfaces /etc/network/interfaces  # Set interfaces for usb0
cp config/dhcpcd.conf /etc/dhcpcd.conf  # Set static IPs for wlan0 and usb0
cp config/resolv.conf /etc/resolv.conf  # Set DNS server
cp config/dhcpd.conf /etc/dhcp/dhcpd.conf  # Set subnet for the DHCP server
cp config/isc-dhcp-server /etc/default/isc-dhcp-server  # Set interface for DHCP server

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

#dhcpcd.conf
_dhcpcd=/etc/dhcpcd.conf # File path
sed -i -r "62,62{s,static ip_address=.*,static ip_address=$_address\/$_CIDRmask,g}" $_dhcpcd

# Down and up adapter for new config to take effect
ip addr flush dev wlan0
ifdown wlan0
ifup wlan0
ifconfig wlan0 up

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

# TODO Comments
if ! uname -a | grep -q "4.4.50+"; then
	BRANCH=master rpi-update 5224108
	reboot now
fi

touch /boot/ssh

if grep -q "usb0" /etc/network/interfaces; then
	echo "usb0 already configured"
else
	cat /home/pi/usbskeletonkey/config/usb0-config | tee --append /etc/network/interfaces > /dev/null
fi

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

mv /home/pi/usbskeletonkey/components/framework/shell_scripts/g_hid.ko /lib/modules/4.4.50+/kernel/drivers/usb/gadget/legacy/g_hid.ko
chmod +x /home/pi/usbskeletonkey/components/framework/shell_scripts/hid-gadget-test

# TODO Test this
# Install python 3.6
# ( cd ~ ;
# bash <(curl -S https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv6l.sh) ;
# ./conda config --add channels rpi ;
# ./conda install python=3.6)

sed -i -r "1,16{s,first_run .*,first_run = false,g}" ./config.ini
