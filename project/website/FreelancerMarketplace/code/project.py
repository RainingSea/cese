class Project:
    def __init__(self, name: str, description: str, assigned_freelancer: str):
        self.name = name
        self.description = description
        self.assigned_freelancer = assigned_freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.assigned_freelancer}\n")

    @staticmethod
    def load_all() -> list:
        projects = []
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, assigned_freelancer = line.strip().split('|')
                    projects.append(Project(name, description, assigned_freelancer))
        except FileNotFoundError:
            pass
        return projects