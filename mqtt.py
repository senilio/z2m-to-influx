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
    timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
    print(f'{timestamp} {text}')

def push_to_influx(x):
    db.write([x],{'db':db_name}, 204, 'line')

def on_connect(client, userdata, flags, rc):
    log("Connected with result code " + str(rc))
    client.subscribe(str(mqtt_topic))

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    for attribute in attributes:
        if attribute in payload:
            log(f'{topic} {attribute}={payload[attribute]}')
            push_to_influx(f'{topic} {attribute}={payload[attribute]}')


# First read environment variables provided by docker
db_name    = os.environ['INFLUX_DB_NAME']
db_host    = os.environ['INFLUX_DB_HOST']
db_port    = os.environ['INFLUX_DB_PORT']
mqtt_host  = os.environ['MQTT_HOST']
mqtt_port  = os.environ['MQTT_PORT']
mqtt_topic = os.environ['MQTT_TOPIC']

# Initialize connection to Influx
db = InfluxDBClient(host=db_host, port=db_port, database=db_name)

# Set up MQTT subscriber
mq = mqtt.Client()
mq.on_connect = on_connect
mq.on_message = on_message
mq.connect(mqtt_host, int(mqtt_port), 60)

# Listen to the subscribed topic forever
mq.loop_forever()
