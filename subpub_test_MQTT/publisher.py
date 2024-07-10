import paho.mqtt.client as mqtt
import time
import math

broker = "localhost"
port = 1883
topic = "sensor/data"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client.on_connect = on_connect
client.connect(broker, port, 60)

while True:
    value = math.sin(0.2*time.time())
    client.publish(topic, value)
    time.sleep(1)
