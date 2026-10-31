class RemoteError(RuntimeError):
    """デバイスサーバー側で発生したエラーの表現。"""
    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        super().__init__(f"{error_type}: {message}")
