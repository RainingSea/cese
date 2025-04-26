class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    def load_projects(self):
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer_id = line.strip().split('|')
                projects.append({'name': name, 'description': description, 'freelancer_id': int(freelancer_id)})
        return projects

    def create_project(self, name: str, description: str, freelancer_id: int) -> bool:
        self.projects.append({'name': name, 'description': description, 'freelancer_id': freelancer_id})
        with open('projects.txt', 'a') as file:
            file.write(f"{name}|{description}|{freelancer_id}\n")
        return True

    def list_projects(self):
        return self.projects