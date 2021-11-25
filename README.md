# z2m-to-influx

This script will subscribe to the MQTT topic which zigbee2mqtt published to. If it finds a device which reports any of the "whitelisted" attributes, it pushes the value to InfluxDB. Once we have the value in InfluxDB, we can easily display the sensors in Grafana.

## Install

Clone the repo

Edit the environment variables in docker-compose.yml

`docker build -t z2m-to-influx .`

Launch the thing with `docker-compose up -d`
