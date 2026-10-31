# 使用方法

```bash
python -m pip install .
```

Brokerを起動してから別々の端末で実行します。

```bash
python examples/server.py
python examples/client.py
```

一対多配信は `Publisher.publish(topic, value)` と `Subscriber.subscribe(topic, callback)` を利用します。両者はRPCとは独立しています。
