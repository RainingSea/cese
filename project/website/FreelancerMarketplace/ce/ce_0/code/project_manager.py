class ProjectManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.projects = self.load_projects()

    def load_projects(self):
        projects = []
        with open(self.file_path, 'r') as file:
            for line in file:
                project_name, description, freelancer = line.strip().split('|')
                projects.append({
                    "project_name": project_name,
                    "description": description,
                    "freelancer": freelancer
                })
        return projects

    def create_project(self, project_name: str, description: str, freelancer: str) -> bool:
        with open(self.file_path, 'a') as file:
            file.write(f"{project_name}|{description}|{freelancer}\n")
        self.projects.append({
            "project_name": project_name,
            "description": description,
            "freelancer": freelancer
        })
        return True

    def get_all_projects(self) -> list:
        return self.projects