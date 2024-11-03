import paho.mqtt.client as mqtt
from config.config import Config
import time

TOPIC = "Test"

def on_connect(client, userdata, flags, rc, properties):
	if rc == 0:
		print("Connected to MQTT Broker!")
		client.subscribe(TOPIC)
	else:
		print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):

	print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 
print(Config.MQTT_USERNAME)
client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
print(Config.MQTT_BROKER)
print(Config.MQTT_PORT)
while True:
	try:
		print("Searching--")
		client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, keepalive=60)
		break;
	except Exception as e:
		print(e)
		time.sleep(2)
client.loop_forever()
