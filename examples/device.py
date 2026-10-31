"""通信方式に依存しないデバイスクラス。"""

class Motor:
    def __init__(self, name="motor1"):
        self.name = name
        self.position = 0.0

    def move(self, position: float) -> float:
        self.position = float(position)
        print(f"[{self.name}] move({position}) -> {self.position}", flush=True)
        return self.position

    def get_position(self) -> float:
        return self.position
