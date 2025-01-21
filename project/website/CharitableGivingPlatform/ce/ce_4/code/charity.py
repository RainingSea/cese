class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def save(self):
        with open('charities.txt', 'a') as file:
            file.write(f"{self.name}|{self.mission}|{','.join(self.projects)}\n")

    @staticmethod
    def load_all():
        charities = []
        with open('charities.txt', 'r') as file:
            for line in file:
                name, mission, projects = line.strip().split('|')
                charities.append(Charity(name, mission, projects.split(',')))
        return charities