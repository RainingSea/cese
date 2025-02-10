class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    @staticmethod
    def load_all() -> list:
        charities = []
        with open('charities.txt', 'r') as file:
            for line in file:
                name, mission, projects = line.strip().split('|')
                projects_list = projects.split(',')
                charities.append(Charity(name, mission, projects_list))
        return charities