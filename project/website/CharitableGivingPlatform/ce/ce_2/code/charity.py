class Charity:
    def __init__(self, name: str, mission: str, projects: list):
        self.name = name
        self.mission = mission
        self.projects = projects

    def get_details(self):
        return f"{self.name}: {self.mission} Projects: {', '.join(self.projects)}"