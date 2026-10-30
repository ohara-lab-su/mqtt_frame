"""通信に依存しないデバイスオブジェクトを公開するMQTTサーバー。"""
from concurrent.futures import ThreadPoolExecutor
import threading
import uuid
import paho.mqtt.client as mqtt
from .codec import encode, decode
from .topics import request, group, event, segment

class MqttDeviceServer:
    def __init__(self, device, name, *, groups=(), host='localhost', port=1883,
                 root='mqtt_frame', methods=None, workers=1, username=None, password=None, tls=False):
        self.device, self.name = device, segment(name)
        self.groups = tuple(segment(x) for x in groups)
        self.root, self.host, self.port = segment(root), host, port
        # 公開メソッドは明示的に指定する。任意のprivate属性やプロパティは公開しない。
        self.methods = set(methods) if methods is not None else {
            n for n in dir(type(device)) if not n.startswith('_') and callable(getattr(type(device), n, None))
        }
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f'srv-{self.name}-{uuid.uuid4().hex[:8]}')
        if username is not None: self._client.username_pw_set(username, password)
        if tls: self._client.tls_set()
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._ready = threading.Event()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure: return
        client.subscribe(request(self.root, self.name), qos=1)
        for name in self.groups: client.subscribe(group(self.root, name), qos=1)
        self._ready.set()

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self._ready.clear()

    def _on_message(self, client, userdata, msg):
        try: data = decode(msg.payload)
        except (ValueError, UnicodeDecodeError): return
        if not isinstance(data, dict) or data.get('v') != 1: return
        # 応答先は同一root配下のreplyトピックに限定する。
        reply_to = data.get('reply_to')
        if not isinstance(reply_to, str) or not reply_to.startswith(f'{self.root}/reply/'):
            return
        if len(reply_to.split('/')) != 3: return
        self._executor.submit(self._dispatch, data, reply_to)

    def _dispatch(self, data, reply_to):
        method = data.get('method')
        response = {'v': 1, 'id': data.get('id'), 'device': self.name}
        try:
            if method not in self.methods or not isinstance(method, str):
                raise AttributeError(f'公開されていないメソッド: {method}')
            args, kwargs = data.get('args', []), data.get('kwargs', {})
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise TypeError('args/kwargsの形式が不正です')
            response.update(ok=True, result=getattr(self.device, method)(*args, **kwargs))
        except Exception as exc:
            response.update(ok=False, error={'type': type(exc).__name__, 'message': str(exc)})
        try: self._client.publish(reply_to, encode(response), qos=1, retain=False)
        except (TypeError, ValueError): pass  # JSON非対応の戻り値は現版では送信できない

    def publish_event(self, name, value):
        return self._client.publish(event(self.root, self.name, name), encode(value), qos=1, retain=False)

    def start(self, timeout=10):
        self._client.connect(self.host, self.port)
        self._client.loop_start()
        if not self._ready.wait(timeout):
            self.close()
            raise ConnectionError('MQTT接続がタイムアウトしました')
        return self

    def close(self):
        self._client.disconnect()
        self._client.loop_stop()
        self._executor.shutdown(wait=True)
        self._ready.clear()

    def __enter__(self): return self.start()
    def __exit__(self, *exc): self.close()
