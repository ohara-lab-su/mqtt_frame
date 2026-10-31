# mqtt_frame

[![en](https://img.shields.io/badge/lang-en-red.svg)](../en/index.html)
[![ja](https://img.shields.io/badge/lang-ja-blue.svg)](../ja/index.html)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fmqtt_frame-181717?logo=github)](https://github.com/ohara-lab-su/mqtt_frame/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](./index.html)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.html)

```{toctree}
:maxdepth: 2

usage
design
api
```

既存のPythonデバイスクラスを変更せず、MQTTで公開するための軽量通信フレームです。単一対象の透過型メソッド呼び出しと、独立したPub/Subを提供します。**試作段階であり、実Broker通信は未検証です。**
