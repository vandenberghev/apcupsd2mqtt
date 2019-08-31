# apcupsd2mqtt
APC UPS stats (fetched from apcaccess - requires apcupsd to run) over MQTT

This script can be run as a service with systemd.

EXAMPLE /lib/systemd/system/apcupsd2mqtt.service:

    [Unit]
    Description=APCUPSD 2 MQTT
    After=network-online.target

    [Service]
    ExecStart=/usr/bin/python3 /home/vince/ups-stats.py
    Restart=on-failure
    Type=idle

    [Install]
    WantedBy=multi-user.target


Steps:

  1. Create the .service file as described above in `/lib/systemd/system/`
  2. `sudo systemctl daemon-reload`
  3. `sudo systemctl enable`
  4. `sudo service apcupsd2mqtt start`
  5. `sudo service apcupsd2mqtt status`
