#!/usr/bin/env python3

'''
Quick 'n dirty :)
This script can be run as a service with systemd.

--- EXAMPLE /lib/systemd/system/apcupsd2mqtt.service ---

[Unit]
Description=APCUPSD 2 MQTT
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 /home/vince/ups-stats.py
Restart=on-failure
Type=idle

[Install]
WantedBy=multi-user.target

--- END EXAMPLE ---

Steps:

  1. Create the .service file as described above in /lib/systemd/system/
  2. sudo systemctl daemon-reload
  3. sudo systemctl enable
  4. sudo service apcupsd2mqtt start
  5. sudo service apcupsd2mqtt status

'''

import subprocess
import time
import paho.mqtt.client as mqtt

# ----- USER CONFIG -----

# MQTT CONFIG
MQTT_BROKER = "your.domain-or-ip.com"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "apcupsd/"
MQTT_KEEPALIVE_INTERVAL = 30

# OTHER CONFIG
POLLING_INTERVAL = 15

# ----- END CONFIG -----

mc = mqtt.Client()
mc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

while True:
    # Fetch the apcupsd status output
    OUTPUT = subprocess.run(['apcaccess'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    d = dict()
    for item in OUTPUT.splitlines():
        s = item.split(":")
        k = s[0].strip()
        v = s[1].strip()
        d[k] = v

    apc_type = d["MODEL"].replace(" ", "-").lower()
    status = d["STATUS"]
    linev = d["LINEV"].split(" ")[0]
    load = d["LOADPCT"].split(" ")[0]
    charge = d["BCHARGE"].split(" ")[0]
    timeleft = d["TIMELEFT"].split(" ")[0]
    battv = d["BATTV"].split(" ")[0]
    nompower = d["NOMPOWER"].split(" ")[0]
    watt = (float(load) / 100) * int(nompower)

    # Publish message to MQTT Topic
    mc.publish(MQTT_TOPIC_PREFIX + "apc_type", apc_type)
    mc.publish(MQTT_TOPIC_PREFIX + "status", status)
    mc.publish(MQTT_TOPIC_PREFIX + "linev", linev)
    mc.publish(MQTT_TOPIC_PREFIX + "load", load)
    mc.publish(MQTT_TOPIC_PREFIX + "charge", charge)
    mc.publish(MQTT_TOPIC_PREFIX + "timeleft", timeleft)
    mc.publish(MQTT_TOPIC_PREFIX + "battv", battv)
    mc.publish(MQTT_TOPIC_PREFIX + "nompower", nompower)
    mc.publish(MQTT_TOPIC_PREFIX + "power", watt)

    mc.loop()
    time.sleep(POLLING_INTERVAL)