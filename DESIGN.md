# 実装・設計引き継ぎ

この版はプロトタイプです。既存フレームの現行ソースを逐語的に比較した互換実装ではありません。

重要な境界：デバイスクラスは通信を知らない。DeviceServerは公開オブジェクトへの呼び出しを中継し、通信依存の要求・応答処理はフレームが担当する。DeviceClientは動的メソッドProxyを提供する。Publisher/Subscriberはデバイスクラスに依存しない。

現状のBは任意Topicへのfan-outのみ。複数DeviceServerが同一Topicを購読してメソッドを呼び出す透過型の一対多操作は未実装。対象列挙・戻り値・部分失敗・重複実行・権限管理を設計する必要がある。

公開前に検証する項目：既存フレームとのAPI整合、MQTT 5 Broker実機接続、RPC競合、切断再接続、QoS、ACL、TLS、型シリアライズ、property、async、デバイス専用pyi。

## Brokerとプロトコル

同梱BrokerはaMQTT 0.12系（MQTT 3.1.1）。クライアントもMQTT 3.1.1で接続し、reply_toとidをJSON本文で伝達する。開発用Brokerは初期状態でループバックにのみbindする。
