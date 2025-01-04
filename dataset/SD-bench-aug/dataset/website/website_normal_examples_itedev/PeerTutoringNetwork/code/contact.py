class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        pass  # Saving is handled in main.py