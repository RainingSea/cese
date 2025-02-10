class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        pass  # Not needed as we handle saving in main.py

    def load(self, username: str):
        pass  # Not needed as we handle loading in main.py