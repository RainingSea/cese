class Project:
    def __init__(self, name: str, description: str, freelancer_assigned: str):
        self.name = name
        self.description = description
        self.freelancer_assigned = freelancer_assigned

    def save(self):
        with open('projects.txt', 'a') as f:
            f.write(f'{self.name}|{self.description}|{self.freelancer_assigned}\n')


class ProjectManager:
    def create_project(self, name: str, description: str, freelancer_assigned: str) -> Project:
        project = Project(name, description, freelancer_assigned)
        project.save()
        return project

    def load_projects(self) -> list:
        projects = []
        try:
            with open('projects.txt', 'r') as f:
                for line in f:
                    name, description, freelancer_assigned = line.strip().split('|')
                    projects.append(Project(name, description, freelancer_assigned))
        except FileNotFoundError:
            pass
        return projects