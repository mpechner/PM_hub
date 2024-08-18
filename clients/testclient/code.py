# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import ipaddress
#import ssl
import wifi
import socketpool
#import adafruit_connection_manager
#import adafruit_requests
import adafruit_minimqtt.adafruit_minimqtt as MQTT

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"pass to {os.getenv('CIRCUITPY_WIFI_PASSWORD')}")
while True:
    try:
        res = wifi.radio.connect(
            os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
        )
    except Exception as ex:
        print(ex)
        sleep(15)
        continue
    break

print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

ping_ip = ipaddress.IPv4Address("192.168.99.2")
ping = wifi.radio.ping(ip=ping_ip)

# retry once if timed out
if ping is None:
    ping = wifi.radio.ping(ip=ping_ip)

if ping is None:
    print("Couldn't ping successfully")
else:
    # convert s to ms
    print(f"Pinging 'google.com' took: {ping * 1000} ms")

pool = socketpool.SocketPool(wifi.radio)
#requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("SERVER_HOST: " +os.getenv("SERVER_HOST") + ":" )

mqttc = MQTT.MQTT(
    broker=os.getenv("SERVER_HOST"),
    port=1883,
    username=MQTT_USER,
    password=MQTT_PASSWORD,
    socket_pool=pool
)

def on_publish(client, userdata,topic, pid  ):
     print("Published to {0} with PID {1}".format(topic, pid))

mqttc.on_publish = on_publish
mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)

mqttc.connect(True, os.getenv("SERVER_HOST"), 1883, 60)

#mqttc.connect()

topic = os.getenv("TOPIC")
mqttc.subscribe(topic)

ii = 0
while True:
    #print(dir(mqttc))
    #print(topic, "foo " + str(ii))
    mqttc.publish(topic, "foo  " + str(ii))

    print(ii)
    time.sleep(5)
    ii += 1
