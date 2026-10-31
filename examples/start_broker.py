"""Pythonから同梱MQTT Brokerを起動する例。

使用例: python examples/start_broker.py --host 127.0.0.1 --port 1883
"""
from mqtt_frame.broker import main

if __name__ == "__main__":
    main()
