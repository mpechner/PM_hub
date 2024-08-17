# PM_hub
Also the parachutemobile-aprs-hub
http://parachutemobile.org

FIRST this is a brain dump and learning state.

Parachute Mobile has had an APRS, aprs.org, radio that has transmitted spO2 along with the location and altitude of the jumper. I have wanted to expand to sensors other than just spO2. Was not possible with the current gear. But with MQTT, the raspberry pi and timy circuit python boards with wifi onboard, it is very possible.

Here is the one gotcha that needs to be tested. Teeny tiny antennas and possible issues with the jumpers body blocking the signal.  So the first test will be mounting the pi on the chest.  Then put the python board at different locations and see what the packet loss is. [Initial Test](Initial_Test.md)

# misc notes

You can read about my [failure to get hostapd running](hostapd-failure.md). I do want to get it running at some point since it is the proper method.

After talking to a friend he convinced me to abandon bluetooth and use wifi.

The client code and paho clients works.

# Setting up Raspberry Pi as a hotspot

I did this instead. I added this line to `/etc/rc.local`

`nmcli device wifi hotspot ssid MY_SSID password MY_PASSWORD`

Since I want the wlan0 ip range to be static I need to try again.
Was given a link to the current version of raspian. Will give this another shot.

# Setup MQTT client board
## Env Setup
Install the circuit python pip wrapper. pipx setups of a venv for python packages the run a commands.  Keeps the smallest venv need for the one command.  pipx by default installs un `~/.local`. Here are the docs\
`https://pypi.org/project/pipx/`

```
pip install pipx
pipx install circup
```
You need to isntall:\
```
circup install adafruit_connection_manager
circup install adafruit_requests
circup install adafruit_minimqtt
circup install adafruit_connection_manager
```

Using https://www.adafruit.com/product/5700

OK, so I could not get the arduino bootloader installed.  Circuit Python it is.

MQTT is the library adafruit ported to circuitpython \
`https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT`

Documentation\
`https://docs.circuitpython.org/projects/minimqtt/en/latest/`



# Setup MQTT Server on the Raspberry Pi
Install and enable mosquitto
```
apt install mosquitto-dev   mosquitto-clients
sudo systemctl enable mosquitto.service
sudo systemctl start mosquitto.service
```

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

# Notes on paho software
https://github.com/eclipse/paho.mqtt.python

https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html

https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/

https://www.emqx.com/en/blog/how-to-use-mqtt-in-python



Install paho to write the code to read messages.  
 `apt install python3-paho-mqtt`
 

