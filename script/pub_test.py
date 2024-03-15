# python 3.6
import random
import time

from paho.mqtt import client as mqtt_client
from mqtt_connect import MqttConnect

if __name__ == '__main__':
    host = '172.17.0.1'
    port = 1883
    client_id = f'publish-{random.randint(0, 1000)}'

    mqtt = MqttConnect(client_id, host, port)
    mqtt.test_publish()
