import paho.mqtt.client as mqtt
import json
import time
import os

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
print("BROKER: " + BROKER_HOST + ":" + str(BROKER_PORT))

LOGGING_TOPIC = "zigbee2mqtt/bridge/logging"

FRIENDLY_NAME = "bulb_1"
DEVICE_TOPIC = "zigbee2mqtt/" + FRIENDLY_NAME
GET_TOPIC = DEVICE_TOPIC + "/get"
SET_TOPIC = DEVICE_TOPIC + "/set"


# exposed:
# brightness 0-254
# color_temp 250 - 454
# state ON / OFF

# todo: synchronize access


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("connected with result code " + str(rc))
    client.subscribe(LOGGING_TOPIC)
    client.subscribe(DEVICE_TOPIC)


def on_message(client, userdata, msg):
    topic: str = msg.topic
    payload: str = msg.payload.decode("utf-8")
    print("received message from: " + topic)
    if FRIENDLY_NAME in topic:
        print("    " + payload)
    if topic == LOGGING_TOPIC and "error" in payload:
        print("ERROR: " + payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


def connect():
    client.connect(BROKER_HOST, BROKER_PORT, 60)


def getState() -> dict:
    state: dict | None = None

    def on_mess(client, userdata, msg) -> None:
        on_message(client, userdata, msg)
        nonlocal state
        state = json.loads(msg.payload.decode("utf-8"))

    client.message_callback_add(DEVICE_TOPIC, on_mess)
    try:
        client.publish(GET_TOPIC, json.dumps({"state": ""}))
        TIMEOUT = 2
        start_time = time.time()
        while True:
            time.sleep(0.01)
            if state is not None or (time.time() - start_time > TIMEOUT):
                return state
    finally:
        client.message_callback_remove(DEVICE_TOPIC)


def setState(state: dict) -> None:
    client.publish(SET_TOPIC, json.dumps(state))
