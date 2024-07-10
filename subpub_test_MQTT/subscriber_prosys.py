import json
import time
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from collections import deque

broker = "localhost"
port = 1883
topic = "prosysopc/json/data/urn:BGO-1043.ad.norceresearch.no:OPCUA:SimulationServer/WriterGroup1/VariableDataSetWriter"
data_queue = deque(maxlen=100)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    jsonmsg = json.loads(msg.payload.decode())
    try:
        # Sometimes, the prosys server provide the wrong nodeid, e.g., Sinusoid is sometimes "i=1004" (sawtooth)
        value = float(jsonmsg["Messages"][0]["Payload"]["Triangle"]["Body"])
        print(value)
        data_queue.append(value)
    except:
        print("An exception happened")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

# Start the loop in a separate thread
client.loop_start()

plt.ion()
fig, ax = plt.subplots()
(line,) = ax.plot(data_queue)

while True:
    if data_queue:
        line.set_ydata(data_queue)
        line.set_xdata(range(len(data_queue)))
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(1)
        # time.sleep(1000)

client.loop_stop()
client.disconnect()
