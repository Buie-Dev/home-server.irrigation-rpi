import paho.mqtt.client as mqtt
from config.config import Config
from Classes.ValveTask import ValveTask
from Classes.ValveScheduler import ValveScheduler
import time
import json

TEST_TOPIC = "Test"
ACTION_TOPIC = 'action'
valve_scheduler = ValveScheduler()

def on_connect(client, userdata, flags, rc, properties):
	if rc == 0:
		print("Connected to MQTT Broker!")
		client.subscribe(TEST_TOPIC)
		client.subscribe(ACTION_TOPIC)
		valve_scheduler.start()
	else:
		print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
	message = msg.payload.decode()
	print(f"Received message '{message}' on topic '{msg.topic}'")
	try:
		json_data = json.loads(msg.payload.decode())
		print(json_data)
		if msg.topic == ACTION_TOPIC:
			task = ValveTask(json_data)
			valve_scheduler.add_new_task(task)

	except Exception as e:
		print("Here---------------")
		print("Error", e)
	








# ----------------- START UP -------------------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) 
client.username_pw_set(Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

while True:
	try:
		print("Searching--")
		client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, keepalive=60)
		break
	except Exception as e:
		print(e)
		time.sleep(2)
client.loop_forever()
