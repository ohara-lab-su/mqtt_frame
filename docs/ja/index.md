# mqtt_frame

MQTTのPub/Subを使って、デバイスクラスに通信依存を導入せず、一対一RPCと一対多RPCを実装します。

## 通信意味論

- Unicast: `call(device, method, ...)` は最初の応答を返す。失敗時は `RpcError`、無応答は `RpcTimeout`。
- Multicast: `multicast(group, method, ..., expected={...})` は期待する全デバイスから応答が来るか期限まで待つ。戻り値は `MulticastResult`。
- `expected=None`: 対象一覧が不明なため期限まで受信する。完全性は保証しない。
- Event: `publish_event(name, value)` と `subscribe(device, name, callback)`。

## 制約

Brokerによる配送確認は装置の実行完了を意味しません。QoS 1では再配送されることがあり、moveなど非冪等な操作を重複実行する可能性があります。現在の実装は重複排除を行いません。安全インターロックには使用しないでください。各装置の制御権・認可・監査ログは別途必要です。

JSONで表現できる引数と戻り値に限定します。同期APIのみです。グループの対象確定・探索は未実装です。

## 構成

`src/mqtt_frame/client.py` はクライアント、`server.py` は装置公開、`topics.py` はトピック、`codec.py` はJSON形式を扱います。

## 利用例

[README](../../README.md)を参照してください。
