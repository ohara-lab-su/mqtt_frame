# Examples / 実行例

[日本語](#日本語) | [English](#english)

## 日本語

このディレクトリには、
既存のPythonデバイスクラスを変更せずにMQTT経由で公開する最小構成の例を収録しています。`device.py` は通信を知らない制御クラスです。
`server.py` が公開し、`client.py` が元のメソッド名で呼び出します。`group_server.py` と `group_client.py` は一対多配信を示します。

### 事前準備

Python 3.10以上と、別途起動したMQTT 5対応Broker（例：Mosquitto）が必要です。Broker自体はPythonパッケージの依存関係に含まれません。Brokerが
`localhost:1883` で稼働していることを確認してください。

リポジトリのルートで以下を実行します。

```bash
python -m pip install .
```

`paho-mqtt` は `pyproject.toml` の通常依存関係として自動導入されます。追加の `pip install paho-mqtt` は不要です。

### 1. 単一デバイスRPC

ターミナル1：

```bash
python examples/server.py
```

ターミナル2：

```bash
python examples/client.py
```

`client.py` は `move(100.0)` と `get_position()` を呼び出します。サーバー停止時はクライアントがタイムアウトします。終了はCtrl+Cです。

### 2. 一対多の同一メソッド配信

別々のターミナルで2台分のDeviceServerを起動します。

```bash
python examples/group_server.py motor1
```

```bash
python examples/group_server.py motor2
```

3つ目のターミナルから一度だけ配信します。

```bash
python examples/group_client.py
```

両サーバーが `devices/_groups/motors/rpc/request` を購読し、`move(100.0)` を受信します。
**この例は要求配信であり、全装置の実行結果を回収するRPCではありません。** Brokerへのpublish成功は装置実行成功を意味しません。QoS
1の再配送による重複実行も排除していません。

### 3. 汎用Pub/Sub

```bash
python examples/broadcast.py
```

`broadcast.py` は `lab/motors/command` にJSONメッセージを送ります。 **このTopicは上記DeviceServerのRPC
Topicとは別物であり、実行例のMotorはこのメッセージで動作しません。** Subscriberを別途用意した場合にのみ受信できます。

### ファイル対応

| ファイル          | 役割                              |
|-------------------|-----------------------------------|
| `device.py`       | 通信非依存のMotorクラス           |
| `server.py`       | 単一デバイスの公開                |
| `client.py`       | 単一デバイスの透過呼び出し        |
| `group_server.py` | グループTopicの購読               |
| `group_client.py` | 一度のpublishで複数デバイスへ要求 |
| `broadcast.py`    | RPCとは独立したPub/Subのpublish   |

## English

These examples expose an existing Python `Motor` class without adding MQTT code to the device class. Python 3.10+ and a
separately running MQTT 5 broker at `localhost:1883` are required.

```bash
python -m pip install .
```

For single-device RPC, start `python examples/server.py` and then `python examples/client.py` in another terminal. For
group delivery, start `python examples/group_server.py motor1` and `python examples/group_server.py motor2` in separate
terminals, then run `python examples/group_client.py`. The group operation delivers a command; it does **not** aggregate
results or guarantee execution. `broadcast.py` demonstrates an independent publish operation, not a device method call.
