from mqtt_frame import MqttDeviceServer

class Motor:
    def move(self, position):
        return {'position': position}

if __name__ == '__main__':
    with MqttDeviceServer(Motor(), 'motor1', groups=['motors'], methods=['move']):
        input('Enterで終了: ')
