"""paho-mqtt 2.xへの薄い接続アダプター。"""
import threading
import paho.mqtt.client as mqtt

class Connection:
    def __init__(self, host="localhost", port=1883, client_id="", *, keepalive=60):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id, protocol=mqtt.MQTTv311)
        self.host, self.port, self.keepalive = host, port, keepalive
        self._connected = threading.Event()
        self._subscriptions = set()
        self._handlers = []
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            return
        self._connected.set()
        for topic, qos in list(self._subscriptions):
            client.subscribe(topic, qos=qos)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        self._connected.clear()

    def _on_message(self, client, userdata, message):
        for handler in tuple(self._handlers):
            handler(message)

    def start(self, timeout=10.0):
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()
        if not self._connected.wait(timeout):
            self.close()
            raise TimeoutError("MQTT Brokerへの接続が確立しませんでした")
        return self

    def subscribe(self, topic, qos=1):
        self._subscriptions.add((topic, qos))
        if self._connected.is_set():
            self.client.subscribe(topic, qos=qos)

    def add_handler(self, handler):
        self._handlers.append(handler)

    def publish(self, topic, payload, qos=1, retain=False, properties=None):
        info = self.client.publish(topic, payload, qos=qos, retain=retain, properties=properties)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise ConnectionError(f"MQTT publish失敗: {info.rc}")
        return info

    def close(self):
        self.client.disconnect()
        self.client.loop_stop()
        self._connected.clear()
