## https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import json
import requests
import csv
from datetime import datetime
import time


# Define Variables

# Ip Adress of the MQTT Broker
MQTT_HOST = "localhost"
# Port used by the MQTT Broker
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
# Name of the tpoc where data will be pushed inside the MQTT Broker
MQTT_TOPIC = "sensor-data"




# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message published with mid", mid)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code :: ", str(rc))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload) # <- do you mean this payload = {...} ?
    payload = json.loads(msg.payload) # you can use json.loads to convert string to json
    print(payload['asset']) # then you can check the value
    client.disconnect() # Got message then disconnect

# Initiate MQTT Client
mqttc = mqtt.Client("mqttx_32bc19a3")

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect with MQTT Broker
print('cici')
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
print('caca')

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# Loop forever
mqttc.loop_start()
# Get a sample dataset
with open('dataset_MP.csv', 'r') as read_obj:
    raw_data = csv.DictReader(read_obj)
    for row in raw_data:
        # row variable is a list that represents a row in csv
        print("waiting 3.5 s")
        time.sleep(3.5)
        print("sending data")
        print(row)
        mqttc.publish(MQTT_TOPIC, json.dumps(row))

mqttc.loop_stop()
mqttc.disconnect()




