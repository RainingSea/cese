class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    @staticmethod
    def load_charities() -> list:
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    projects_list = projects.split(',')
                    charities.append(Charity(name, mission, projects_list))
        except FileNotFoundError:
            pass
        return charities