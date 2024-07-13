# PM_hub
parachutemobile-aprs-hub

You can read about my failure to get hostapd running on hostapd-fail.md. I do want to get it running at some point since it is the proper method.

After talking to a friend he convinced me to abandon bluetooth and use wifi.

# Setting up Raspberry Pi as a hotspot

I did this instead. I added this line to `/etc/rc.local`

`nmcli device wifi hotspot ssid MY_SSID password MY_PASSWORD`

# 
