class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        with open('projects.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.freelancer}\n")


class ProjectManager:
    def create_project(self, name: str, description: str, freelancer: str) -> None:
        project = Project(name, description, freelancer)
        project.save()

    def load_projects(self) -> list:
        projects = []
        try:
            with open('projects.txt', 'r') as f:
                for line in f:
                    name, description, freelancer = line.strip().split('|')
                    projects.append(Project(name, description, freelancer))
        except FileNotFoundError:
            pass
        return projects