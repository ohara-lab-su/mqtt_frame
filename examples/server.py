import time
from device import Motor
from mqtt_frame import DeviceServer

server = DeviceServer(Motor(), "motor1").start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    server.close()
