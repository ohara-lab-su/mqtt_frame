# mqtt_frame

MQTT Brokerを介したデバイス向け通信フレーム。単一デバイスRPC、複数デバイスへの一斉RPC、イベント配信を提供します。デバイスクラスはMQTTをimportしません。

**状態:** 0.1.0 初期実装。既存のgrpc_frame/ese774_frameとのAPI互換性は未検証です。実機制御に投入する前に接続試験・認可・再送対策が必要です。

## インストール

```bash
pip install .
```

## 使用例

サーバー:

```python
from mqtt_frame import MqttDeviceServer

class Motor:
    def move(self, position):
        return {"position": position}

with MqttDeviceServer(Motor(), "motor1", groups=["motors"], methods=["move"]):
    input("Enterで終了")
```

クライアント:

```python
from mqtt_frame import MqttClient

with MqttClient() as client:
    print(client.call("motor1", "move", 100))
    print(client.multicast("motors", "move", 100, expected={"motor1"}).responses)
```

`expected`を指定しないmulticastはタイムアウトまで応答を収集します。各応答には`ok`/`result`または`error`が含まれます。応答がないことは未実行を意味しません。

## ドキュメント

- [日本語](docs/ja/index.md)
- [English](docs/en/index.md)
- [GitHub Pages](https://ohara-lab-su.github.io/mqtt_frame/)

Apache-2.0。詳しくは[LICENSE](LICENSE)。
