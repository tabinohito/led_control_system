import random
import time
import logging

from paho.mqtt import client as mqtt_client

class MqttConnect:
    def __init__(self, client_id, host, port = 1883):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.client = self.connect_mqtt()

        # defined number
        self.FIRST_RECONNECT_DELAY = 1
        self.RECONNECT_RATE = 2
        self.MAX_RECONNECT_COUNT = 12
        self.MAX_RECONNECT_DELAY = 60

    def on_disconnect(self,client, userdata, rc):
        logging.info("Disconnected, Error code: %s", rc)
        reconnect_count, reconnect_delay = 0, self.FIRST_RECONNECT_DELAY
        while reconnect_count < self.MAX_RECONNECT_COUNT:
            logging.info("Reconnect after %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnection succeeded!")
                return
            except Exception as err:
                logging.error("%s. Reconnection failed. Will try again...", err)

            reconnect_delay *= self.RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, self.MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnection failed after %s attempts. Terminating..." , reconnect_count)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,self.client_id)
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.connect(self.host, self.port)
        return client

    def publish(self, topic, msg):
        result = self.client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def subscribe(self,topic):
        self.client.subscribe(topic)
        self.client.on_message = self.on_message

    def loop_forever(self):
        self.client.loop_forever()

    def test_publish(self):
        msg_count = 1
        while True:
            time.sleep(1)
            topic = "python/mqtt"
            msg = f"messages: {msg_count}"
            self.publish(topic, msg)
            
            msg_count += 1
            if msg_count > 5:
                break

    def test_subscribe(self):
        topic = "python/mqtt"
        self.subscribe(topic)
        self.loop_forever()

