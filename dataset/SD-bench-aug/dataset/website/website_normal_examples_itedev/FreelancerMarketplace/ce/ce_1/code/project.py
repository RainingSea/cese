class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        # This method is not used in this implementation as we save directly to the file
        pass

    @staticmethod
    def load_all() -> list:
        # This method is not used in this implementation as we load projects directly in main.py
        pass