"""同梱のaMQTT Brokerを起動するコマンド。"""
import argparse
import asyncio
import logging
from amqtt.broker import Broker


async def serve(host: str = "127.0.0.1", port: int = 1883) -> None:
    """MQTT 3.1.1 Brokerを起動し、終了時に停止する。"""
    config = {
        "listeners": {"default": {"type": "tcp", "bind": f"{host}:{port}"}},
        "plugins": {
            "amqtt.plugins.authentication.AnonymousAuthPlugin": {"allow_anonymous": True},
            "amqtt.plugins.topic_checking.TopicTabooPlugin": {},
        },
    }
    broker = Broker(config)
    await broker.start()
    print(f"MQTT Broker 起動: {host}:{port}", flush=True)
    try:
        await asyncio.Event().wait()
    finally:
        await broker.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="mqtt_frame 同梱 MQTT Broker (開発用)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=1883)
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(serve(args.host, args.port))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
