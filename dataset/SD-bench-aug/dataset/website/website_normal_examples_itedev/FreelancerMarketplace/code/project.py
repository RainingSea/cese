class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.freelancer}\n")

    @staticmethod
    def load_all() -> list:
        return []  # Loading is handled in main.py