
# Some tests when learning OPC UA

## Tools

Python libs: `pip install opcua paho-mqtt`

Prosys OPC UA simulation server: https://downloads.prosysopc.com/opc-ua-simulation-server-downloads.php

mosquitto (the MQTT broker): https://github.com/eclipse/mosquitto

## Tests

### Test 1. Hello world: with an online OPC UA server

Run helloworld_milo.py to connect with [milo OPC UA server](https://github.com/eclipse/milo)

### Test 2. Hello world: with a local OPC UA server (Prosys)

1. Run Prosys OPC UA simulation server
2. Run helloworld_prosys.py

### Test 3. Read data: with a local OPC UA server (Python)

1. Run server_test.py
2. Run client_test.py

This is to retrieve data by calling `get_value()` periodically. The followings are to retrieve data using Sub/Pub mode.

### Test 4. Sub/Pub: over opc.tcp

1. Run server_test.py 
2. Run client_subpub_opctcp.py

ChatGPT: The `opcua` library primarily supports the client-server model over TCP, so for Pub/Sub over UDP, additional steps and potentially different libraries are needed. Using OPC UA Pub/Sub over UDP in Python requires either specific support in your chosen library or the use of a C library like Open62541 with appropriate bindings. 

`class SubHandler()` is from python lib opcua, for Sub/Pub over TCP.

### Test 5. Sub/Pub: over MQTT, using mosquitto_pub and mosquitto_sub

1. Run in shell: `mosquitto`
2. Run in shell: `mosquitto_sub -t "test/topic" -v`
3. Run in shell: `mosquitto_pub -t "test/topic" -m "hello world"`

See: [eclipse/mosquitto: Eclipse Mosquitto - An open source MQTT broker (github.com)](https://github.com/eclipse/mosquitto?tab=readme-ov-file#quick-start). It is better to use `"` instead of `'`, as it seems they can make differences.

### Test 6. Sub/Pub: over MQTT, using paho.mqtt and mosquitto_sub

1. Run in shell: `mosquitto`
2. Run publisher.py
3. Run in shell:
```shell
mosquitto_sub -t "sensor/data" -v
```

In this test, paho.mqtt.client.publish() as publisher, mosquitto_sub as subscriber.

### Test 7. Sub/Pub: over MQTT, using paho.mqtt

1. Run in shell: `mosquitto`
2. Run publisher.py
3. Run subscriber.py
In this test, paho.mqtt.client.publish() is used as publisher, subscribe() as subscriber.

### Test 8. Sub/Pub: over MQTT, using Prosys simulation server

1. Run in shell: `mosquitto`
2. Run Prosys simulation server, and set up in the PubSub tab, 
    1. Key settings include address, encoding. 
    2. The queue name is the topic name.
    3. Test it with `mosquitto_sub -t "prosysopc/json/data/urn:BGO-1043.ad.norceresearch.no:OPCUA:SimulationServer/WriterGroup1/VariableDataSetWriter" -v`
3. Run subscriber.py

In this test, Prosys simulation server is used as publisher, subscribe() as subscriber.
