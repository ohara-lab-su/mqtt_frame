"""MQTTの配送と独立した要求・応答メッセージ形式。"""
import json
from typing import Any

def dumps(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")

def loads(value: bytes) -> Any:
    return json.loads(value.decode("utf-8"))

def device_topic(namespace: str, device: str) -> str:
    if not namespace or not device or any(c in device for c in "/+#"):
        raise ValueError("namespace と device は有効なMQTTトピック要素で指定してください")
    if any(c in namespace for c in "+#"):
        raise ValueError("namespace にワイルドカードは指定できません")
    return f"{namespace.strip('/')}/{device}/rpc/request"
