import json
from models import User, Project, Freelancer

class DataManager:
    def __init__(self, users_file: str, projects_file: str, freelancers_file: str):
        self.users_file = users_file
        self.projects_file = projects_file
        self.freelancers_file = freelancers_file

    def load_users(self) -> list:
        try:
            with open(self.users_file, 'r') as file:
                return [User(**json.loads(line)) for line in file]
        except FileNotFoundError:
            return []

    def save_user(self, user: User):
        with open(self.users_file, 'a') as file:
            file.write(json.dumps(user.to_dict()) + "\n")

    def load_projects(self) -> list:
        try:
            with open(self.projects_file, 'r') as file:
                return [Project(**json.loads(line)) for line in file]
        except FileNotFoundError:
            return []

    def save_project(self, project: Project):
        with open(self.projects_file, 'a') as file:
            file.write(json.dumps(project.to_dict()) + "\n")

    def load_freelancers(self) -> list:
        try:
            with open(self.freelancers_file, 'r') as file:
                return [Freelancer(**json.loads(line)) for line in file]
        except FileNotFoundError:
            return []

    def save_freelancer(self, freelancer: Freelancer):
        with open(self.freelancers_file, 'a') as file:
            file.write(json.dumps(freelancer.to_dict()) + "\n")