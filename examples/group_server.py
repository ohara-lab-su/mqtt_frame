"""別ターミナルで複数起動し、同一グループへの一斉要求を受信する。"""
import argparse
import time
from device import Motor
from mqtt_frame import DeviceServer

parser = argparse.ArgumentParser()
parser.add_argument("name")
args = parser.parse_args()
server = DeviceServer(Motor(), args.name, groups=("motors",)).start()
print(f"{args.name}: group motors を購読中")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    server.close()
