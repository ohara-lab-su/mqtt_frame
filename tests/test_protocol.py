from mqtt_frame.protocol import dumps, loads, device_topic

def test_json_roundtrip():
    assert loads(dumps({"value": "日本語"})) == {"value": "日本語"}

def test_topic():
    assert device_topic("devices", "motor1") == "devices/motor1/rpc/request"
