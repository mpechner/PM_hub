#!/bin/bash

# Check if the script is running as root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root. Please use sudo or switch to the root user."
  exit 1
fi


# Configure iptables for network routing
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# Allow SSH and MQTT ports (22 and 1883) on all interfaces
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 1883 -j ACCEPT

#allow mDNS
iptables -A INPUT -p udp --dport 5353 -d 224.0.0.251 -j ACCEPT
iptables -A INPUT -p udp --dport 5353 -d 224.0.0.251 -j ACCEPT
iptables -A OUTPUT -p udp --dport 5353 -d 224.0.0.251 -j ACCEPT


# Save iptables rules
sh -c "iptables-save > /etc/iptables/rules.v4"

