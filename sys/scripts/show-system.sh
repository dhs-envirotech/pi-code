#!/usr/bin/bash

echo -n "HOSTNAME: "
hostname

echo

echo -n "IP: "
ifconfig | grep netmask | grep broadcast

echo

# Display the OS
cat /etc/os-release | grep PRETTY | perl -p -i -e 's/PRETTY/OS/g' 2>/dev/null

# display the hardware

cat /proc/cpuinfo | grep Model

echo
echo "avalable memory: total  used available %"
 df --total | grep total
