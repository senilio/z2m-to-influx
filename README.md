# z2m-to-influx

This script will subscribe to the MQTT topic which zigbee2mqtt publishes to. If it finds a device which reports any of the whitelisted attributes, it pushes those value to InfluxDB. Once we have the value in InfluxDB, we can easily display the sensors in Grafana.

InfluxDB column names will correspond to the MQTT topic, and will contain a field for each attribute we're saving, like temperature and humidity etc.

## Install

1. Clone the repo
2. Edit the environment variables in docker-compose.yml
3. `docker build -t z2m-to-influx .`
4. Launch the thing with `docker-compose up -d`
