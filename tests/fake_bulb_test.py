import time
import src.bulb_control as bc


def test():

    bc.connect()
    bc.client.loop_start()

    while not bc.client.is_connected():
        time.sleep(0.05)

    try:
        _test_setter_getter()
        print("\n  -> all tests successful")
    finally:
        bc.client.loop_stop()
        print("\ndone")


def _test_setter_getter():

    bc.setState({"state": "OFF"})
    result = bc.getState()
    assert result["state"] == "OFF"

    bc.setState({"state": "TOGGLE"})
    result = bc.getState()
    assert result["state"] == "ON"

    bc.setState({"state": "OFF"})
    result = bc.getState()
    assert result["state"] == "OFF"

    bc.setState({"state": "ON"})
    result = bc.getState()
    assert result["state"] == "ON"

    bc.setState({"state": "TOGGLE"})
    result = bc.getState()
    assert result["state"] == "OFF"

    bc.setState({"brightness": 254})
    result = bc.getState()
    assert result["state"] == "OFF"  # still
    assert result["brightness"] == 254

    bc.setState({"brightness": 125})
    result = bc.getState()
    assert result["brightness"] == 125

    bc.setState({"color_temp": 454})
    result = bc.getState()
    assert result["color_temp"] == 454

    bc.setState({"color_temp": 267})
    result = bc.getState()
    assert result["color_temp"] == 267
