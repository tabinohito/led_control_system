# python3.6
import random

from paho.mqtt import client as mqtt_client
from mqtt_connect import MqttConnect

if __name__ == '__main__':
    host = '172.17.0.1'
    port = 1883
    topic = "python/mqtt"
    client_id = f'subscribe-{random.randint(0, 100)}'

    mqtt = MqttConnect(client_id, host, port)
    mqtt.test_subscribe()
    mqtt.loop_forever()
    


