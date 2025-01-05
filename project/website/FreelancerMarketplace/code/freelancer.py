class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        pass  # Saving is handled in DataManager

    @staticmethod
    def load(name: str):
        pass  # Loading is handled in DataManager