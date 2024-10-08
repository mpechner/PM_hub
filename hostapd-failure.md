This failed. I was using notes for the wrong release. going to tray again using bookworm specific notes https://raspberrytips.com/access-point-setup-raspberry-pi/
Use the hostapd section

For dhcp use this link. The dhcps server notes are incorrect. 

There is no dhcp serever.
https://www.server-world.info/en/note?os=Debian_12&p=dhcp&f=1

# Network manager Changes
https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/configuring-networkmanager-to-ignore-certain-devices_configuring-and-managing-networking#permanently-configuring-a-device-as-unmanaged-in-networkmanager_configuring-networkmanager-to-ignore-certain-devices

Provided the information for this change
```
[keyfile]
unmanaged-devices=interface-name:wlan0
```

# marks Notes:
/etc/hostap/hostap.conf
```
interface=wlan0_ap
ssid=pistar
hw_mode=g
macaddr_acl=0
auth_algs=1
channel=6
wpa=0
wpa_passphrase=raspberry
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

# hostapd -failed
I tried to setup hostapd and the connecrtion never worked.

Not documented was the change to NetworkManager to remove wlan0 and disabling wpa_supplicant so hostapd would even run.


I asked chatgpt "can I setup the raspbetrry pi to be an wifi AP, then using the  ethernet port on my home network to ssh into it"
Also asked "what is the bibliography for this response"

## bibliography
* hostpad https://w1.fi/hostapd/
* dnsmasq http://www.thekelleys.org.uk/dnsmasq/doc.html
* debian wiki wifi notes https://wiki.debian.org/WiFi/HowToUse
* Raspberry pi not in making it an AP https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md
* bookworm specific: https://raspberrytips.com/access-point-setup-raspberry-pi/

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
