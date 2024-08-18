# PM_hub
Also the parachutemobile-aprs-hub
http://parachutemobile.org

FIRST this is a brain dump and learning state.

Parachute Mobile has had an APRS, aprs.org, radio that has transmitted spO2 along with the location and altitude of the jumper. I have wanted to expand to sensors other than just spO2. Was not possible with the current gear. But with MQTT, the raspberry pi and timy circuit python boards with wifi onboard, it is very possible.

Here is the one gotcha that needs to be tested. Teeny tiny antennas and possible issues with the jumpers body blocking the signal.  So the first test will be mounting the pi on the chest.  Then put the python board at different locations and see what the packet loss is. [Initial Test](Initial_Test.md)

To see the progress, look here [Status](Status.md)

# Raspberry Pi 5 Setup

I loaded the headless 64bit raspian.

I made heavy use of chatgpt for the initial bootstrap.  I had to be able to start the problem clearly. Still had issues around getting wlan0 to come up and act as a correct access point.

The final configuration is piconfig/wifi_ap_setup.sh
Set up the MQTT password:

`mosquitto_sub -h localhost -u parachutemobile -P parachutemobile  -v -t timer`

After it started, it is accepting MQTT packets via wlan0 from the qt board.  Able to SSH in to wifi or eth0.  From wifi, access the internet. So all good.


# misc notes

You can read about my [failure to get hostapd running](hostapd-failure.md). I do want to get it running at some point since it is the proper method.

After talking to a friend he convinced me to abandon bluetooth and use wifi.

The client code and paho clients works.

# Setup MQTT client board
## Env Setup
Install the circuit python pip wrapper. pipx setups of a venv for python packages the run a commands.  Keeps the smallest venv need for the one command.  pipx by default installs un `~/.local`. 
Here are the docs\
`https://pypi.org/project/pipx/`

```
pip install pipx
pipx install circup
```
## Install Libraries
You need to install:\
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


# Notes on paho software
PAHO is what I am using forraspberry pi MQTT development.
* https://github.com/eclipse/paho.mqtt.python
* https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html
* https://cedalo.com/blog/configuring-paho-mqtt-python-client-with-examples/
* https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

Install paho to write the code to read messages.  
 `apt install python3-paho-mqtt`
 
