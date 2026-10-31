# mqtt_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://ohara-lab-su.github.io/mqtt_frame/en/index.html)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](https://ohara-lab-su.github.io/mqtt_frame/ja/index.html)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fmqtt_frame-181717?logo=github)](https://github.com/ohara-lab-su/mqtt_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/mqtt_frame/index.html)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)

```{toctree}
:maxdepth: 2

en/usage
en/design
en/api
```

A lightweight MQTT transport for existing Python device classes. The device class does not depend on MQTT. Transparent single-target method invocation and independent native Pub/Sub are provided. **Testing phase: basic operation has been tested with an MQTT broker; broader validation is still required.**

## Bundled MQTT broker

`pip install .` installs `amqtt` (MQTT 3.1.1 broker) and `paho-mqtt` automatically. Start the local development broker with `mqtt-frame-broker` (default `127.0.0.1:1883`), or run `python examples/start_broker.py`. Authentication is disabled by default: do not expose this listener to untrusted networks. The RPC reply topic and correlation ID are carried in the JSON payload for MQTT 3.1.1 compatibility.
