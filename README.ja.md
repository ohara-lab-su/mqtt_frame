# mqtt_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/mqtt_frame/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/ohara-lab-su/mqtt_frame/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fmqtt_frame-181717?logo=github)](https://github.com/ohara-lab-su/mqtt_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/mqtt_frame/ja/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.html)

> **試作段階（実運用非推奨）**
>
> MQTT Brokerを使用した実通信試験は未実施です。再送・切断・多数接続・異常系の検証も完了していません。

既存のPython制御クラスを通信方式から独立させたまま、MQTTで公開するための軽量な通信フレームです。`ese774_frame`、`grpc_frame`と並ぶ独立した選択肢です。

- 透過型RPC：既存の制御クラスを `DeviceServer` に渡し、`DeviceClient` から元のメソッド名で呼び出します。
- MQTT Pub/Sub：`Publisher` と `Subscriber` でRPCと独立した一対多配信を行います。
- 一対多の**デバイスメソッド呼び出し**は、今後の設計対象であり、この版では未実装です。

```bash
python -m pip install .
```

実行方法：[examples/README.md](examples/README.md)

設計と制約：[docs/ja/design.md](docs/ja/design.md)


[Examples / 実行例](examples/README.md) · [Documentation / ドキュメント](https://ohara-lab-su.github.io/mqtt_frame/)

## MQTT Broker の導入と起動

`pip install .` または PyPI 公開後の `pip install mqtt-frame` で、`paho-mqtt` と Python 製 Broker `amqtt` が通常依存関係として同時にインストールされます。追加の Broker インストールは不要です。

```bash
pip install .
mqtt-frame-broker
```

別の端末でサーバーとクライアントを起動します。起動スクリプト `python examples/start_broker.py` も使用できます。初期設定は `127.0.0.1:1883` で、ローカル開発用の認証なし接続です。外部公開しないでください。

**プロトコル:** 同梱 Broker の aMQTT は MQTT 3.1.1 対応であり、MQTT 5.0 対応ではありません。そのためフレーム側も MQTT 3.1.1 を使用し、RPC の返信先と要求IDはメッセージ本文で管理します。
