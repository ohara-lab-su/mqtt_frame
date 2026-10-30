from mqtt_frame import MqttClient

if __name__ == '__main__':
    with MqttClient() as client:
        print(client.call('motor1', 'move', 100))
        print(client.multicast('motors', 'move', 100, expected={'motor1'}))
