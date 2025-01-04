class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def to_string(self) -> str:
        return f"{self.name}|{self.subject}"