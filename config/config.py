import os
from dotenv import load_dotenv
load_dotenv()
print("---------------")
print(os.getenv("MQTT_PORT"))
class Config:
	MQTT_BROKER = os.getenv("MQTT_BROKER")
	MQTT_PORT = int(os.getenv("MQTT_PORT"))
	MQTT_USERNAME = os.getenv("MQTT_USERNAME")
	MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


