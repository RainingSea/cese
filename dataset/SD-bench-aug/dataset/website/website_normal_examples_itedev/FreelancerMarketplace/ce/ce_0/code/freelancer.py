class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        # This method is not used in this implementation as we save directly to the file
        pass

    @staticmethod
    def load_all() -> list:
        # This method is not used in this implementation as we load freelancers directly in main.py
        pass