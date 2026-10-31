"""既存Pythonオブジェクトを公開するMQTT DeviceServer。"""
from .transport import Connection
from .protocol import dumps, loads, device_topic

class DeviceServer:
    def __init__(self, device, name: str, *, host="localhost", port=1883, namespace="devices", client_id="", groups=()):
        self.device = device
        self.request_topic = device_topic(namespace, name)
        self.group_topics = {f"{namespace.strip(chr(47))}/_groups/{group}/rpc/request" for group in groups}
        self.connection = Connection(host, port, client_id=client_id or f"server-{name}")
        self.connection.add_handler(self._on_message)

    def start(self):
        self.connection.subscribe(self.request_topic)
        for topic in self.group_topics:
            self.connection.subscribe(topic)
        self.connection.start()
        return self

    def _on_message(self, message):
        if message.topic != self.request_topic and message.topic not in self.group_topics:
            return
        try:
            request = loads(message.payload)
            request_id = request.get("id")
            method = request["method"]
            if not isinstance(method, str) or method.startswith("_"):
                raise AttributeError("公開されていないメソッドです")
            target = getattr(self.device, method)
            if not callable(target):
                raise TypeError("属性の読み取りにはget_propertyを使用してください")
            result = target(*request.get("args", []), **request.get("kwargs", {}))
            response = {"id": request_id, "ok": True, "result": result}
        except Exception as exc:
            response = {"id": request.get("id") if isinstance(locals().get("request"), dict) else None,
                        "ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}}
        properties = getattr(message, "properties", None)
        response_topic = getattr(properties, "ResponseTopic", None)
        if response_topic:
            try:
                payload = dumps(response)
            except (TypeError, ValueError) as exc:
                payload = dumps({"id": response["id"], "ok": False,
                                 "error": {"type": type(exc).__name__, "message": str(exc)}})
            self.connection.publish(response_topic, payload, qos=1)

    def close(self):
        self.connection.close()
