class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        pass  # Not needed for this implementation

    @staticmethod
    def load_all() -> list:
        return []  # Not needed for this implementation