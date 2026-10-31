"""RPCと独立したMQTT標準の一対多配信。"""
from .transport import Connection
from .protocol import dumps, loads

class Publisher:
    def __init__(self, *, host="localhost", port=1883, client_id=""):
        self.connection = Connection(host, port, client_id=client_id)

    def start(self):
        self.connection.start()
        return self

    def publish(self, topic, value, *, qos=1, retain=False):
        return self.connection.publish(topic, dumps(value), qos=qos, retain=retain)

    def close(self):
        self.connection.close()

class Subscriber:
    def __init__(self, *, host="localhost", port=1883, client_id=""):
        self.connection = Connection(host, port, client_id=client_id)
        self._callbacks = []
        self.connection.add_handler(self._dispatch)

    def subscribe(self, topic, callback, *, qos=1):
        self._callbacks.append((topic, callback))
        self.connection.subscribe(topic, qos=qos)
        return self

    def _dispatch(self, message):
        import paho.mqtt.client as mqtt
        for topic, callback in tuple(self._callbacks):
            if mqtt.topic_matches_sub(topic, message.topic):
                callback(message.topic, loads(message.payload))

    def start(self):
        self.connection.start()
        return self

    def close(self):
        self.connection.close()
