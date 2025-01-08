class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.freelancer}\n")

    @staticmethod
    def load_projects():
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append(Project(name, description, freelancer))
        return projects