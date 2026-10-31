# mqtt_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://ohara-lab-su.github.io/mqtt_frame/en/index.html)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://ohara-lab-su.github.io/mqtt_frame/ja/index.html)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fmqtt_frame-181717?logo=github)](https://github.com/ohara-lab-su/mqtt_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/mqtt_frame/index.html)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.html)

```{toctree}
:maxdepth: 2

usage
design
api
```

既存のPythonデバイスクラスを変更せず、MQTTで公開するための軽量通信フレームです。単一対象の透過型メソッド呼び出しと、独立したPub/Subを提供します。**テストフェーズです。MQTT Brokerを使用した最低限の動作テストは実施済みですが、追加検証が必要です。**

## MQTT Broker の導入と起動

`pip install .` または PyPI 公開後の `pip install mqtt-frame` で、`paho-mqtt` と Python 製 Broker `amqtt` が通常依存関係として同時にインストールされます。追加の Broker インストールは不要です。

```bash
pip install .
mqtt-frame-broker
```

別の端末でサーバーとクライアントを起動します。起動スクリプト `python examples/start_broker.py` も使用できます。初期設定は `127.0.0.1:1883` で、ローカル開発用の認証なし接続です。外部公開しないでください。

**プロトコル:** 同梱 Broker の aMQTT は MQTT 3.1.1 対応であり、MQTT 5.0 対応ではありません。そのためフレーム側も MQTT 3.1.1 を使用し、RPC の返信先と要求IDはメッセージ本文で管理します。
