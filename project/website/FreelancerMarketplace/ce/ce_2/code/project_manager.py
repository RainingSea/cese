from project import Project

class ProjectManager:
    def __init__(self):
        self.projects = []

    def load_projects(self):
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, assigned_freelancer = line.strip().split('|')
                self.add_project(Project(name, description, assigned_freelancer))

    def save_projects(self):
        with open('projects.txt', 'w') as file:
            for project in self.projects:
                file.write(f"{project.name}|{project.description}|{project.assigned_freelancer}\n")

    def add_project(self, project: Project):
        self.projects.append(project)
        self.save_projects()

    def get_projects(self) -> list[Project]:
        return self.projects