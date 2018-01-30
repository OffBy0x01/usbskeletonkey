#!/usr/bin/env bash
# MUST run as root!

# Install Requirements
apt-get update
# Ensure Python is installed
apt-get --assume-yes install isc-dhcp-server
apt-get --assume-yes install dsniff
apt-get --assume-yes install screen

# compgen -c | grep "mkfs\."