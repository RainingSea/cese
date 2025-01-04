class Project:
    def __init__(self, project_name: str, description: str, assigned_freelancer: str):
        self.project_name = project_name
        self.description = description
        self.assigned_freelancer = assigned_freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.project_name}|{self.description}|{self.assigned_freelancer}\n")

    @staticmethod
    def load_all():
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                project_data = line.strip().split('|')
                projects.append(Project(project_data[0], project_data[1], project_data[2]))
        return projects