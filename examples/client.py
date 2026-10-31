from mqtt_frame import DeviceClient

client = DeviceClient("motor1").start()
try:
    print(client.move(100.0))
    print(client.get_position())
finally:
    client.close()
