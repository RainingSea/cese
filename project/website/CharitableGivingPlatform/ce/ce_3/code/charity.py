class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def save(self):
        with open('charities.txt', 'a') as file:
            projects_str = ','.join(self.projects)
            file.write(f"{self.name}|{self.mission}|{projects_str}\n")

    @staticmethod
    def load_all():
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects_str = line.strip().split('|')
                    projects = projects_str.split(',')
                    charities.append(Charity(name, mission, projects))
        except FileNotFoundError:
            pass
        return charities