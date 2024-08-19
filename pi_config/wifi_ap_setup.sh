#!/bin/bash

# Check if the script is running as root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root. Please use  or switch to the root user."
  exit 1
fi


# Update system packages
 apt-get update && sudo apt-get upgrade -y

# Install necessary packages
 apt install -y firmware-brcm802111 nmap 
 apt-get install -y hostapd dnsmasq iptables-persistent dhcpcd5 vim lsof

# Stop services for configuration
 systemctl stop hostapd
 systemctl stop dnsmasq
 systemctl stop dhcpcd

# Configure static IP for wlan0
cat <<EOF |  tee /etc/dhcpcd.conf
interface wlan0
static ip_address=192.168.99.2/24
static routers=192.168.99.1
static domain_name_servers=192.168.99.1 8.8.8.8
nohook wpa_supplicant
EOF

# Restart dhcpcd service
systemctl enable  dhcpcd
systemctl start dhcpcd 

# Configure DHCP server (dnsmasq)
 mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat <<EOF |  tee /etc/dnsmasq.conf
interface=wlan0
dhcp-range=192.168.99.120,192.168.99.150,255.255.255.0,24h
EOF

# Configure hostapd (Wi-Fi AP)
cat <<EOF |  tee /etc/hostapd/hostapd.conf
interface=wlan0
ssid=jumpera
hw_mode=g
channel=7
wmm_enabled=1
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
 sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

# Step 2: Add delay to Mosquitto service
echo "Adding 20-second delay to Mosquitto service..."
mkdir -p /etc/systemd/system/mosquitto.service.d
cat <<EOF > /etc/systemd/system/mosquitto.service.d/override.conf
[Unit]
After=hostapd.service
Requires=hostapd.service
[Service]
ExecStartPre=/bin/sleep 20
EOF

# Step 3: Reload systemd to apply the changes
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable IP forwarding
sed -i 's|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|' /etc/sysctl.conf
sysctl -p

mkdir -p /etc/systemd/system/hostapd.service.d
cat <<EOF > /etc/systemd/system/hostapd.service.d/override.conf
[Unit]
After=dhcpcd.service
Requires=dhcpcd.service
[Service]
ExecStartPre=/bin/sleep 10
EOF

echo "Reloading systemd daemon..."
systemctl daemon-reload

# Enable and start services
systemctl unmask hostapd
systemctl enable hostapd
systemctl enable dnsmasq
systemctl start hostapd
systemctl start dnsmasq
systemctl start dhcpcd
systemctl enable dhcpcd



apt install -y mosquitto-dev   mosquitto-clients

# mqtt setup
mkdir /var/cache/mosquitto/
chmod 0755 /var/cache/mosquitto/

touch /etc/mosquitto/passwd
chmod 0644  /etc/mosquitto/passwd

cat <<EOF |  tee /etc/mosquitto/conf.d/extra.conf
per_listener_settings true
allow_anonymous false
listener 1883 0.0.0.0
persistence true
autosave_interval  600
log_timestamp true
log_timestamp_format %Y-%m-%dT%H:%M:%S
password_file /etc/mosquitto/passwd
persistence_file /var/cache/mosquitto/mosquitto.db
EOF


systemctl enable mosquitto.service
systemctl start mosquitto.service

