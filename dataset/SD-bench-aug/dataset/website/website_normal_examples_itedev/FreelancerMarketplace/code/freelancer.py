class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        pass  # Saving is handled in main.py

    @staticmethod
    def load_all() -> list:
        return []  # Loading is handled in main.py