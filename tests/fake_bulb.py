import json

import paho.mqtt.client as mqtt

import src.bulb_control as bc

# todo: render current state


def info(message: str):
    print("fake_bulb: " + message)


state = {
    "state": "ON",  # TOGGLE
    "brightness": 171,
    "color_temp": 454,
}


def get_state(client: mqtt.Client, userdata, msg):
    on_message(client, userdata, msg)
    client.publish(bc.DEVICE_TOPIC, json.dumps(state))


def set_state(client: mqtt.Client, userdata, msg):
    global state
    on_message(client, userdata, msg)
    info("old state: " + json.dumps(state))
    payload: str = msg.payload.decode("utf-8")
    new_state: dict = json.loads(payload)
    # todo: input validation
    # special handling for "TOGGLE"
    if new_state.get("state", None) == "TOGGLE":
        old_status = state["state"]
        new_status = "ON" if old_status == "OFF" else "OFF"
        new_state["state"] = new_status
    state |= new_state
    info("  -> new state: " + json.dumps(state))


def on_connect(client: mqtt.Client, userdata, flags, rc):
    info("connected with result code " + str(rc))
    # client.subscribe(bc.DEVICE_TOPIC)
    client.subscribe(bc.GET_TOPIC)
    client.subscribe(bc.SET_TOPIC)
    client.message_callback_add(bc.SET_TOPIC, set_state)
    client.message_callback_add(bc.GET_TOPIC, get_state)


def on_message(client, userdata, msg):
    topic: str = msg.topic
    info("received message from: " + topic)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


def connect():
    client.connect(bc.BROKER_HOST, bc.BROKER_PORT)
