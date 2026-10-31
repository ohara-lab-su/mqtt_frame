# mqtt_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/mqtt_frame/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://github.com/ohara-lab-su/mqtt_frame/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fmqtt_frame-181717?logo=github)](https://github.com/ohara-lab-su/mqtt_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/mqtt_frame/en/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)

> **Testing phase**
>
> Basic operation has been tested with an MQTT broker. Further validation is required for reconnection, redelivery, multiple concurrent clients, and error handling. The package is not yet validated for production use.

Lightweight MQTT communication frame for existing Python device classes, alongside `ese774_frame` and `grpc_frame`. Device classes remain independent of communication. Dynamic single-device RPC and independent native Pub/Sub are provided. Group method-request delivery is available via `GroupPublisher` and `DeviceServer(groups=...)`; response aggregation and exactly-once execution are not implemented.

```bash
python -m pip install .
```

[Examples](examples/README.md) · [Design](docs/en/design.md) · [Documentation](https://ohara-lab-su.github.io/mqtt_frame/en/)


[Examples / 実行例](examples/README.md) · [Documentation / ドキュメント](https://ohara-lab-su.github.io/mqtt_frame/)

## Bundled MQTT broker

`pip install .` installs `amqtt` (MQTT 3.1.1 broker) and `paho-mqtt` automatically. Start the local development broker with `mqtt-frame-broker` (default `127.0.0.1:1883`), or run `python examples/start_broker.py`. Authentication is disabled by default: do not expose this listener to untrusted networks. The RPC reply topic and correlation ID are carried in the JSON payload for MQTT 3.1.1 compatibility.
