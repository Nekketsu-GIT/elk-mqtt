import paho.mqtt.client as mqttClient
import time
import requests
import json
from elasticsearch import Elasticsearch


es = Elasticsearch("http://localhost:9200")


# Define on_publish event function
def on_publish(client, userdata, mid):
    print (client, "Message published with mid : ", mid)
  
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
  
def on_message(client, userdata, message):
    
    # evaluate data
    data = json.loads(message.payload)
    print("Message received: ", data)
    to_send = {
        "Air temperature": data["Air temperature"],
        "Process temperature": data["Process temperature"],
        "Rotational speed": data["Rotational speed"],
        "Torque": data["Torque"],
        "Tool wear": data["Tool wear"]
    }
    headers = {'content-type': 'application/json'}
    r1 = requests.post('http://localhost:9200/main_preds/_doc?pipeline=machine-failure-classification', data=json.dumps(to_send), headers=headers)
    

    resp = es.get(index="main_preds", id=json.loads(r1.content)["_id"])
    mf = resp['_source']['Machine failure']['Machine failure_prediction']

    print("Prediction:", mf)

    if(mf == True):
        # Publish stop message
        print("Stoping machine")
        client.publish("stop", json.dumps(resp['_source']['Machine failure']))


  
Connected = False   #global variable for the state of the connection
  
broker_address= "localhost"  #Broker address
port = 1883                         #Broker port

  
client = mqttClient.Client("Python subscribe")               #create new instance
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("sensor-data-test")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()