class NotExists(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg