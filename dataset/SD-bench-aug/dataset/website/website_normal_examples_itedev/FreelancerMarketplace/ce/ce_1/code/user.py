class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        # This method is not used in this implementation as we save directly to the file
        pass

    @staticmethod
    def load_all() -> list:
        # This method is not used in this implementation as we load users directly in main.py
        pass