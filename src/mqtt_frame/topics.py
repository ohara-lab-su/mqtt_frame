"""MQTTトピック生成。"""

def segment(value):
    if not isinstance(value, str) or not value or any(c in value for c in '/+#\x00'):
        raise ValueError("トピック要素に / + # NUL または空文字は使えません")
    return value

def request(root, device):
    return f"{root}/rpc/{segment(device)}/request"

def group(root, name):
    return f"{root}/group/{segment(name)}/request"

def reply(root, client):
    return f"{root}/reply/{segment(client)}"

def event(root, device, name):
    return f"{root}/event/{segment(device)}/{segment(name)}"
