class Session:
    def __init__(self):
        self.current_user = None

    def set_user(self, username: str) -> None:
        self.current_user = username

    def clear_user(self) -> None:
        self.current_user = None

    def get_user(self) -> str:
        return self.current_user