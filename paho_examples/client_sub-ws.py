#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

import context  # Ensures paho is in PYTHONPATH
import hidden
import json
import paho.mqtt.client as mqtt
from os import makedirs, chmod
import datetime
from paho_examples.hidden import MQTT_LOGDIR


def on_connect(mqttc, obj, flags, reason_code):
    print("reason_code: " + str(reason_code))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "topic" : msg.topic,
        "message": str(msg.payload)
        }
    fipath = MQTT_LOGDIR + '/' + msg.topic
    with open(fipath, 'a+') as topicqueue:
        json.dump(log_entry,topicqueue)
        topicqueue.write("\n")

def on_subscribe(mqttc, obj, mid, reason_code_list):
    print("Subscribed: " + str(mid) + " " + str(reason_code_list))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
makedirs(MQTT_LOGDIR,exist_ok=True)
chmod(MQTT_LOGDIR, 0o0755)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
mqttc.username_pw_set(hidden.MQTT_USER, hidden.MQTT_PASSWORD)
# mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
mqttc.on_log = on_log
mqttc.connect(hidden.MQTT_HOST, 1883, 60)
mqttc.message_callback_add("tuple", on_message)
mqttc.message_callback_add("timer", on_message)
mqttc.subscribe("#", 2)

mqttc.loop_forever()
