import os
import json
import datetime
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

#################################################
# What attributes are we interested in?
attributes = ["power", "temperature", "humidity"]
#################################################

def log(text):
    timestamp = '[{:%Y-%m-%d %H:%M:%S.%f}]'.format(datetime.datetime.now())
    print(f'{timestamp} {text}')

def push_to_influx(x):
    client.write([x],{'db':db_name}, 204, 'line')

def on_connect(client, userdata, flags, rc):
    log("Connected with result code " + str(rc))
    client.subscribe("zigbee2mqtt/+")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    for attribute in attributes:
        if attribute in payload:
            log(f'{topic} {attribute}={payload[attribute]}')
            push_to_influx(f'{topic} {attribute}={payload[attribute]}')


def main():
    # First read environment variables provided by docker
    db_name    = os.environ['INFLUX_DB_NAME']
    db_host    = os.environ['INFLUX_DB_HOST']
    db_port    = os.environ['INFLUX_DB_PORT']
    mqtt_host  = os.environ['MQTT_HOST']
    mqtt_port  = os.environ['MQTT_PORT']
    mqtt_topic = os.environ['MQTT_TOPIC']

    # Initialize connection to Influx
    client = InfluxDBClient(host=db_host, port=db_port, database=db_name)

    # Set up MQTT subscriber
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_host, mqtt_port, 60)

    client.loop_forever()

if __name__ == '__main__':
    main()
