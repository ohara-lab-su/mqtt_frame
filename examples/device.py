class Motor:
    def __init__(self):
        self.position = 0.0

    def move(self, position: float) -> float:
        self.position = position
        return self.position

    def get_position(self) -> float:
        return self.position
