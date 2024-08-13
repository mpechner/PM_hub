#!/bin/bash

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install necessary packages
sudo apt-get install -y hostapd dnsmasq iptables-persistent

# Stop services for configuration
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Configure static IP for wlan0
cat <<EOF | sudo tee /etc/dhcpcd.conf
interface wlan0
    static ip_address=192.168.99.2/24
    nohook wpa_supplicant
EOF

# Restart dhcpcd service
sudo service dhcpcd restart

# Configure DHCP server (dnsmasq)
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat <<EOF | sudo tee /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.99.120,192.168.99.150,255.255.255.0,24h
EOF

# Configure hostapd (Wi-Fi AP)
cat <<EOF | sudo tee /etc/hostapd/hostapd.conf
interface=wlan0
ssid=jumpera
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=parachutemobile_rules_a
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# Point hostapd to the config file
sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# Enable IP forwarding
sudo sed -i 's|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|' /etc/sysctl.conf
sudo sysctl -p

# Configure iptables for network routing
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# Allow SSH and MQTT ports (22 and 1883) on all interfaces
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT

# Save iptables rules
sudo sh -c "iptables-save > /etc/iptables/rules.v4"

# Enable and start services
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo systemctl start hostapd
sudo systemctl start dnsmasq
