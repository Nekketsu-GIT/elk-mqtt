## https://pypi.org/project/paho-mqtt/
import paho.mqtt.client as mqtt
import pandas as pd
import time
import logging
import threading
import json
from sklearn.utils import resample


# Get dataset
raw_data = pd.read_csv('resamples_dataset.csv')

raw_data.reset_index()

raw_data['Machine failure'] = raw_data['Machine failure'].astype('bool')
raw_data['TWF'] = raw_data['TWF'].astype('bool')
raw_data['HDF'] = raw_data['HDF'].astype('bool')
raw_data['PWF'] = raw_data['PWF'].astype('bool')
raw_data['OSF'] = raw_data['OSF'].astype('bool')
raw_data['RNF'] = raw_data['RNF'].astype('bool')

sensor_type = ["L","M","H"]


# Define Variables

# Ip Adress of the MQTT Broker
MQTT_HOST = "localhost"
# Port used by the MQTT Broker
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
# Name of the tpoc where data will be pushed inside the MQTT Broker
#MQTT_TOPIC = "sensor-data"
MQTT_TOPIC = "sensor-data-test"


# Define on_publish event function
def on_publish(client, userdata, mid):
    print (client, "Message published with mid : ", mid)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(client, "Connected to MQTT Broker with result code :: ", str(rc))
    
def on_message(client, userdata, message):
    mqttc.disconnect()
    

# Our sensor routine
def sensor_function(name):
    

    
    logging.info("sensor %s: starting", name)
    
    #Get a random sample of our raw data
    sensor_data = raw_data[raw_data.Type==name]
    sensor_data.drop('Product ID', inplace=True, axis=1)
    sensor_data.reset_index()

    # Initiate MQTT Client
    mqttc = mqtt.Client(name)
    mqttc.subscribe("stop")
    
    # Register publish callback function
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect

    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    mqttc.loop_start()

    for index, row in sensor_data.iterrows():
        json_data = json.loads(row.to_json())
        time.sleep(3.5)
        print(json.dumps(json_data))
        mqttc.publish(MQTT_TOPIC, json.dumps(json_data))

    mqttc.loop_stop()
    mqttc.disconnect()
    
    logging.info("sensor %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = list()
    for index in sensor_type:
        logging.info("Main    : create and start sensor %s.", index)
        x = threading.Thread(target=sensor_function, args=(index,))
        threads.append(x)
        x.start()

    for index, sensor in enumerate(threads):
        logging.info("Main    : before joining sensor %s.", index)
        sensor.join()
        logging.info("Main    : sensor %s done", index)


















