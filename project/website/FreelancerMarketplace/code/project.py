class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        pass  # Saving is handled in DataManager

    @staticmethod
    def load(name: str):
        pass  # Loading is handled in DataManager