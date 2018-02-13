#!/usr/bin/env bash

ip addr flush dev wlan0  # Flush wlan0

# Down and up adapter for new config to take effect
ifdown wlan0
ifup wlan0
ifconfig wlan0 up
