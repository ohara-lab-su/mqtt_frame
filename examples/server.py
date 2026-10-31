"""単一デバイス用サーバー。"""
import time
from device import Motor
from mqtt_frame import DeviceServer

def main():
    server = DeviceServer(Motor("motor1"), "motor1").start()
    print("[motor1] MQTT接続・購読開始", flush=True)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

if __name__ == "__main__":
    main()
