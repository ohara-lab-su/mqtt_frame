# Examples / 実行例

[日本語](#日本語) | [English](#english)

## 日本語

### 準備（Brokerもpipでインストールされます）

Python 3.10以降を使用します。リポジトリのルートで次を実行してください。

```bash
python -m pip install .
```

`pyproject.toml` の通常依存関係に `paho-mqtt` と `amqtt` が含まれます。別途Mosquittoをインストールする必要はありません。**Brokerはインストールだけでは起動しません。** 以下の手順で起動します。

### 1. PythonスクリプトからBrokerを起動（ターミナル1）

リポジトリのルートで次を実行します。

```bash
python examples/start_broker.py
```

`start_broker.py` は `mqtt_frame.broker.main()` を呼び出し、Python製aMQTT Brokerを `127.0.0.1:1883` で起動します。終了は Ctrl+C です。引数も渡せます。

```bash
python examples/start_broker.py --host 127.0.0.1 --port 1883
```

インストール時に登録されるコマンドから起動する場合は、次と等価です。**両方を同時に起動しないでください**（ポートが競合します）。

```bash
mqtt-frame-broker
```

### 2. 単一デバイスのメソッド呼び出し

Brokerを起動したまま、ターミナル2でサーバーを起動します。

```bash
python examples/server.py
```

ターミナル3でクライアントを実行します。

```bash
python examples/client.py
```

`client.py` は `motor1` に対して `move(100.0)` と `get_position()` を実行します。`device.py` の `Motor` はMQTTに依存しません。

### 3. 一対多のメソッド配信（主用途）

単一デバイスのサーバーを停止してから、**Brokerは起動したまま**、別々のターミナルで次を実行します。

ターミナル2：

```bash
python examples/group_server.py motor1
```

ターミナル3：

```bash
python examples/group_server.py motor2
```

両サーバーの購読開始を確認してから、ターミナル4で一度だけ要求を発行します。

```bash
python examples/group_client.py
```

`motors` グループの両サーバーに `move(100.0)` が配送され、それぞれのサーバー端末に `move(...)` の実行ログが表示されます。グループ要求は**応答を集約しません**。publish完了は各デバイスでの実行成功を保証しません。また、QoS 1での重複配送を排除していないため、実装例をそのまま実機の危険な操作に使用しないでください。

### 4. 汎用Pub/Sub

Brokerを起動した状態で、次を実行できます。

```bash
python examples/broadcast.py
```

これは `lab/motors/command` へJSONをpublishする独立した例です。上記のDeviceServerはこのTopicを購読しないため、Motorは動作しません。

### 構成

| ファイル | 用途 |
| --- | --- |
| `start_broker.py` | PythonからBrokerを起動 |
| `device.py` | 通信非依存のMotor |
| `server.py`, `client.py` | 一対一のRPC |
| `group_server.py`, `group_client.py` | 一対多の同一メソッド配信 |
| `broadcast.py` | 独立したPub/Sub publish |

Brokerは開発用の匿名接続で、初期設定ではローカルホストのみにbindします。外部ネットワークへ公開する場合は認証・TLS・アクセス制御を別途設計してください。

## English

### Installation and broker startup

From the repository root (Python 3.10+):

```bash
python -m pip install .
```

Both `paho-mqtt` and the Python broker `amqtt` are installed as standard dependencies. **Installation does not automatically start the broker.** Open terminal 1 and run:

```bash
python examples/start_broker.py
```

This runs the bundled broker on `127.0.0.1:1883`. You can alternatively use `mqtt-frame-broker`, but do not run both at once. Stop it with Ctrl+C.

### Single-device RPC

In terminal 2:

```bash
python examples/server.py
```

In terminal 3:

```bash
python examples/client.py
```

The client invokes `move(100.0)` and `get_position()` on `motor1`. The `Motor` class contains no MQTT code.

### One-to-many method delivery

Stop the single-device server, but leave the broker running. In two separate terminals:

```bash
python examples/group_server.py motor1
```

```bash
python examples/group_server.py motor2
```

Once both servers have subscribed, run in a fourth terminal:

```bash
python examples/group_client.py
```

Both servers should print their `move(100.0)` execution. Group delivery does **not** aggregate responses or guarantee device execution. QoS 1 may redeliver commands.

### Independent Pub/Sub

```bash
python examples/broadcast.py
```

This publishes to `lab/motors/command`, which the example device servers do not subscribe to. The default broker allows anonymous local connections and must not be exposed to untrusted networks.
