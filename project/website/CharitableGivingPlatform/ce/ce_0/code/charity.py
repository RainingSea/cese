class Charity:
    def __init__(self, id: str, name: str, mission: str, projects: str):
        self.id = id
        self.name = name
        self.mission = mission
        self.projects = projects

    @staticmethod
    def load_all() -> list:
        charities = []
        with open('charities.txt', 'r') as file:
            for line in file:
                id, name, mission, projects = line.strip().split('|')
                charities.append(Charity(id, name, mission, projects))
        return charities