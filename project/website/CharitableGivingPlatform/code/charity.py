class Charity:
    def __init__(self, name: str, mission: str):
        self.name = name
        self.mission = mission
        self.projects = []

    def add_project(self, project: str):
        self.projects.append(project)

    def get_details(self) -> dict:
        return {
            'name': self.name,
            'mission': self.mission,
            'projects': self.projects
        }

    @staticmethod
    def load_charities() -> list:
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission = line.strip().split('|')
                    charities.append(Charity(name, mission))
        except FileNotFoundError:
            return []
        return charities