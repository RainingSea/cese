class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def save(self):
        with open('charities.txt', 'a') as file:
            file.write(f"{self.name}|{self.mission}|{'|'.join(self.projects)}\n")

    @staticmethod
    def load_all():
        charities = []
        try:
            with open('charities.txt', 'r') as file:
                for line in file:
                    name, mission, projects = line.strip().split('|')
                    projects_list = projects.split('|') if projects else []
                    charities.append(Charity(name, mission, projects_list))
        except FileNotFoundError:
            pass
        return charities