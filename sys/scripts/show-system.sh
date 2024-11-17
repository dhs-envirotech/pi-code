#!/usr/bin/bash

# Display the OS
cat /etc/os-release | grep PRETTY | perl -p -i -e 's/PRETTY/OS/g' 2>/dev/null

# display the hardware

cat /proc/cpuinfo | grep Model
