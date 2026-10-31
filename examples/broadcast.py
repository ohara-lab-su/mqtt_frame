"""同じTopicを購読する全デバイスに同じ要求を配信する例。"""
from mqtt_frame import Publisher

publisher = Publisher().start()
try:
    publisher.publish("lab/motors/command", {"command": "stop"}, retain=False)
finally:
    publisher.close()
