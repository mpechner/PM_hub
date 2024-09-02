# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import ipaddress
import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import microcontroller
import traceback

def MQTT_connect(mqtt):
    if mqtt.is_connected():
        return

    conn_retry = 0
    while ( conn_retry < 3 ):
        ret =  mqtt.reconnect()
        if ret == 0:
            return
        print("conn error: ", ret)
        mqtt.disconnect()
        time.sleep(5)
        conn_retry = conn_retry + 1
    print("more than 3 reconnects: " , conn_retry)

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"pass to {os.getenv('CIRCUITPY_WIFI_PASSWORD')}")
attempts=0

while True:
    print("SSID:" + os.getenv("CIRCUITPY_WIFI_SSID") + "  pass:" + os.getenv("CIRCUITPY_WIFI_PASSWORD") + ':')
    try:
        res = wifi.radio.connect(
            os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
        )
    except Exception as ex:
        print("wifi connect fail " + str(attempts) + "  " + str(ex))

        if attempts == 5:
            microcontroller.reset()
        attempts = attempts + 1
        time.sleep(5)

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



#MQTT_connect(mqttc)
mqttc.connect()
topic = os.getenv("TOPIC")
mqttc.subscribe(topic)

try:
 ii = 0
 while True:
    MQTT_connect(mqttc)
    #print(dir(mqttc))
    #print(topic, "foo " + str(ii))
    print("is connected? ", mqttc.is_connected())
    mqttc.publish(topic, "foo  " + str(ii))

    print(ii)
    time.sleep(5)
    ii += 1
except Exception as ex:
    print("loop fail:" + str(ex))
    print('{} encountered, exiting: {}\n{}'.format(type(ex), ex, traceback.format_exception(ex)))
    time.sleep(30)
    #microcontroller.reset()

