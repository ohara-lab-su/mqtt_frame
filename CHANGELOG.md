# Changelog

## 0.1.0 (experimental)

- Pythonデバイスクラスの動的RPC公開とクライアントProxyを試作。
- MQTT 5 Response Topic / Correlation Dataによる単一対象RPCを実装。
- RPCと独立したPublisher / Subscriberを追加。
- 英語・日本語Sphinxドキュメント、GitHub Pages、PyPI公開ワークフローを追加。
- 一対多デバイスRPC、property透過化、実Broker試験は未完了。

- aMQTT Brokerを通常依存関係に追加し、`mqtt-frame-broker` 起動コマンドを提供。
- MQTT 3.1.1 に通信プロトコルを統一し、返信先を本文で管理。

- examples/README.md をBrokerのPythonスクリプト起動から一対一・一対多の実行順序まで日英で改訂。docs/ja・docs/en の使用方法にも反映。
