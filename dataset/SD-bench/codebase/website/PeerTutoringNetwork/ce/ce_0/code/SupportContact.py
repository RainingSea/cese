class SupportContact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def to_string(self) -> str:
        return f"{self.name}|{self.email}|{self.message}"