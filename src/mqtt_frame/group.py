"""複数デバイスに対する同一要求の配信（応答集約なし）。"""
import uuid
from .transport import Connection
from .protocol import dumps

class GroupPublisher:
    """グループTopicへメソッド実行要求を一度だけpublishする。"""
    def __init__(self, *, host="localhost", port=1883, namespace="devices", client_id=""):
        self.namespace = namespace.strip("/")
        self.connection = Connection(host, port, client_id=client_id)

    def start(self):
        self.connection.start()
        return self

    def call(self, group: str, method: str, *args, **kwargs):
        if not group or any(c in group for c in "/+#"):
            raise ValueError("groupは単一のTopic要素で指定してください")
        if not method or method.startswith("_"):
            raise ValueError("公開メソッド名を指定してください")
        topic = f"{self.namespace}/_groups/{group}/rpc/request"
        payload = dumps({"id": uuid.uuid4().hex, "method": method, "args": args, "kwargs": kwargs})
        return self.connection.publish(topic, payload, qos=1, retain=False)

    def close(self):
        self.connection.close()
