"""JSONメッセージの符号化。独自オブジェクトは受け付けない。"""
import json

def encode(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")

def decode(data):
    return json.loads(data)
