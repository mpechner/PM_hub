# PM_hub
parachutemobile-aprs-hub

You can read about my failure to get hostapd running on hostapd-fail.md. I do want to get it running at some point since it is the proper method.

After talking to a friend he convinced me to abandon bluetooth and use wifi.

# Setting up Raspberry Pi as a hotspot

I did this instead. I added this line to `/etc/rc.local`

`nmcli device wifi hotspot ssid MY_SSID password MY_PASSWORD`

# setup MQTT client
Using https://www.adafruit.com/product/5700
As this is a simple read data and publish using mqtt over wifi, arduino is perfect for this task.
https://docs.arduino.cc/tutorials/uno-wifi-rev2/uno-wifi-r2-mqtt-device-to-device/

# Setup MQTT Server on the Raspbetty Pi
apt install mosquitto-dev   mosquitto-clients
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service

created a extra conf file `/etc/mosquitto/conf.d/extra.conf` with the contents

```
per_listener_settings true
allow_anonymous false
listener 1883
password_file /etc/mosquitto/passwd
```
Restarted the mosquitto.service

Setup a user and password
sudo mosquitto_passwd -c /etc/mosquitto/passwd parachutemobile

Install paho to write the code to read messages.  
 `apt install python3-paho-mqtt`
 

