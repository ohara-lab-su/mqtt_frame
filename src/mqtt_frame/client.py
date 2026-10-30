"""単一対象RPC、グループ配信RPC、イベント購読。"""
from dataclasses import dataclass, field
import threading
import time
import uuid
import paho.mqtt.client as mqtt
from .codec import encode, decode
from .topics import request, group, reply, event, segment

class RpcError(RuntimeError):
    pass
class RpcTimeout(TimeoutError):
    pass

@dataclass
class MulticastResult:
    responses: dict = field(default_factory=dict)
    expected: set | None = None
    @property
    def missing(self):
        return set() if self.expected is None else self.expected - self.responses.keys()

class MqttClient:
    """同期API。multicastのexpectedを指定すると全応答またはtimeoutまで待つ。"""
    def __init__(self, host='localhost', port=1883, *, root='mqtt_frame', client_id=None,
                 username=None, password=None, tls=False, keepalive=60):
        self.root = segment(root)
        self.client_id = client_id or uuid.uuid4().hex
        segment(self.client_id)
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.client_id)
        if username is not None: self._client.username_pw_set(username, password)
        if tls: self._client.tls_set()
        self._host, self._port, self._keepalive = host, port, keepalive
        self._pending = {}
        self._lock = threading.RLock()
        self._ready = threading.Event()
        self._callbacks = {}
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect

    def connect(self, timeout=10):
        self._client.connect(self._host, self._port, self._keepalive)
        self._client.loop_start()
        if not self._ready.wait(timeout):
            self.close()
            raise ConnectionError('MQTT接続がタイムアウトしました')
        return self

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure: return
        client.subscribe(reply(self.root, self.client_id), qos=1)
        with self._lock:
            for topic in self._callbacks: client.subscribe(topic, qos=1)
        self._ready.set()

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self._ready.clear()

    def _on_message(self, client, userdata, msg):
        try: payload = decode(msg.payload)
        except (ValueError, UnicodeDecodeError): return
        if msg.topic == reply(self.root, self.client_id):
            req_id = payload.get('id')
            with self._lock:
                item = self._pending.get(req_id)
                if item is not None:
                    item['responses'][payload.get('device')] = payload
                    item['event'].set()
        else:
            with self._lock: callbacks = list(self._callbacks.get(msg.topic, ()))
            for callback in callbacks:
                try: callback(payload)
                except Exception: pass  # ユーザーコールバックでMQTT受信を停止させない

    def _call(self, topic, method, args, kwargs, timeout, expected):
        if not self._ready.is_set(): raise ConnectionError('MQTTに接続されていません')
        req_id = uuid.uuid4().hex
        pending = {'event': threading.Event(), 'responses': {}}
        with self._lock: self._pending[req_id] = pending
        try:
            msg = {'v': 1, 'id': req_id, 'method': method, 'args': list(args),
                   'kwargs': kwargs, 'reply_to': reply(self.root, self.client_id)}
            info = self._client.publish(topic, encode(msg), qos=1, retain=False)
            if info.rc != mqtt.MQTT_ERR_SUCCESS: raise ConnectionError(f'publish失敗: {info.rc}')
            deadline = time.monotonic() + timeout
            while True:
                with self._lock: responses = dict(pending['responses'])
                if expected is None and responses: return next(iter(responses.values()))
                if expected is not None and set(expected) <= responses.keys(): return responses
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    if expected is None: raise RpcTimeout(f'RPC応答なし: {method}')
                    return responses
                pending['event'].wait(remaining)
                pending['event'].clear()
        finally:
            with self._lock: self._pending.pop(req_id, None)

    def call(self, device, method, *args, timeout=10.0, **kwargs):
        response = self._call(request(self.root, device), method, args, kwargs, timeout, None)
        if not response.get('ok'):
            err = response.get('error', {})
            raise RpcError(f"{err.get('type', 'RemoteError')}: {err.get('message', '')}")
        return response.get('result')

    def multicast(self, group_name, method, *args, expected=None, timeout=10.0, **kwargs):
        """expected=Noneの場合、timeoutまで応答を集める。応答数の保証はない。"""
        if expected is not None:
            expected = set(expected)
            if not expected: raise ValueError('expectedは空集合にできません')
        # 未知の参加者数に対しては、タイムアウトまで全応答を収集する。
        if expected is None:
            expected = set()
            collect_all = True
        else: collect_all = False
        if not collect_all:
            raw = self._call(group(self.root, group_name), method, args, kwargs, timeout, expected)
        else:
            raw = self._collect(group(self.root, group_name), method, args, kwargs, timeout)
        return MulticastResult(responses=raw, expected=None if collect_all else expected)

    def _collect(self, topic, method, args, kwargs, timeout):
        req_id = uuid.uuid4().hex
        pending = {'event': threading.Event(), 'responses': {}}
        with self._lock: self._pending[req_id] = pending
        try:
            msg = {'v': 1, 'id': req_id, 'method': method, 'args': list(args),
                   'kwargs': kwargs, 'reply_to': reply(self.root, self.client_id)}
            info = self._client.publish(topic, encode(msg), qos=1)
            if info.rc != mqtt.MQTT_ERR_SUCCESS: raise ConnectionError(f'publish失敗: {info.rc}')
            deadline = time.monotonic() + timeout
            while (remaining := deadline - time.monotonic()) > 0:
                pending['event'].wait(remaining)
                pending['event'].clear()
            with self._lock: return dict(pending['responses'])
        finally:
            with self._lock: self._pending.pop(req_id, None)

    def subscribe(self, device, name, callback):
        topic = event(self.root, device, name)
        with self._lock:
            self._callbacks.setdefault(topic, []).append(callback)
        if self._ready.is_set(): self._client.subscribe(topic, qos=1)

    def close(self):
        self._client.disconnect()
        self._client.loop_stop()
        self._ready.clear()

    def __enter__(self): return self.connect()
    def __exit__(self, *exc): self.close()
