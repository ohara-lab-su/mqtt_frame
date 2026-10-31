"""動的ディスパッチによる透過型RPCクライアント。"""
import threading
import uuid
from .transport import Connection
from .protocol import dumps, loads, device_topic
from .errors import RemoteError

class DeviceClient:
    def __init__(self, name: str, *, host="localhost", port=1883, namespace="devices", client_id=""):
        self.request_topic = device_topic(namespace, name)
        self.client_id = client_id or f"client-{uuid.uuid4().hex}"
        self.response_topic = f"{namespace.strip('/')}/_reply/{self.client_id}"
        self.connection = Connection(host, port, client_id=self.client_id)
        self._pending = {}
        self._lock = threading.Lock()
        self.connection.add_handler(self._on_message)

    def start(self):
        self.connection.subscribe(self.response_topic)
        self.connection.start()
        return self

    def _on_message(self, message):
        if message.topic != self.response_topic:
            return
        try:
            response = loads(message.payload)
            with self._lock:
                pending = self._pending.get(response["id"])
            if pending is not None:
                pending["response"] = response
                pending["event"].set()
        except (ValueError, KeyError, TypeError):
            return

    def call(self, method, *args, timeout=10.0, **kwargs):
        request_id = uuid.uuid4().hex
        pending = {"event": threading.Event(), "response": None}
        with self._lock:
            self._pending[request_id] = pending
        try:
            self.connection.publish(self.request_topic, dumps({"id": request_id, "method": method,
                                                                "args": args, "kwargs": kwargs, "reply_to": self.response_topic}))
            if not pending["event"].wait(timeout):
                raise TimeoutError(f"MQTT RPC応答タイムアウト: {method}")
            response = pending["response"]
            if not response["ok"]:
                error = response["error"]
                raise RemoteError(error["type"], error["message"])
            return response["result"]
        finally:
            with self._lock:
                self._pending.pop(request_id, None)

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        def invoke(*args, **kwargs):
            return self.call(name, *args, **kwargs)
        return invoke

    def close(self):
        self.connection.close()

DeviceProxy = DeviceClient
