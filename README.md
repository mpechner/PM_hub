# PM_hub
parachutemobile-aprs-hub

After talking to a friend he convinced me to abandon bluetooth and use wifi.

# Setting up Raspberry Pi as a AP
I asked chatgpt "can I setup the raspbetrry pi to be an wifi AP, then using the  ethernet port on my home network to ssh into it"
Also asked "what is the bibliography for this response"

## bibliography
* hostpad https://w1.fi/hostapd/
* dnsmasq http://www.thekelleys.org.uk/dnsmasq/doc.html
* debian wiki wifi notes https://wiki.debian.org/WiFi/HowToUse
* Raspberry pi not in making it an AP https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

## turn off wpa_supplicatnad and reomve wlan0 from NetworkManager

## presented steps

```
sudo apt update
sudo apt upgrade
```

```
sudo apt install hostapd dnsmasq
```

edit /etc/dhcpcd.conf and add the following contents
```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

edit /etc/hostapd/hostapd.conf set the file contents to be
```
interface=wlan0
driver=nl80211
ssid=Your_SSID
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=Your_Passphrase
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Configure dnsmasq

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```

Edit /etc/dnsmasq.conf and  set the range.  make sure you are good with the choose IP range.
```
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```

Start the Services

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```
```
sudo reboot
```
