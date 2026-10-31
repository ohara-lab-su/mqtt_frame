"""グループ motors の購読サーバー。"""
import argparse
import time
from device import Motor
from mqtt_frame import DeviceServer

def main():
    parser = argparse.ArgumentParser(description="グループ配信用デバイスサーバー")
    parser.add_argument("name", help="例: motor1 または motor2")
    args = parser.parse_args()
    server = DeviceServer(Motor(args.name), args.name, groups=("motors",)).start()
    print(f"[{args.name}] MQTT接続・購読開始", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

if __name__ == "__main__":
    main()
