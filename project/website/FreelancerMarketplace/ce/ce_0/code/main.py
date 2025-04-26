import os

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.project_manager = ProjectManager()
        self.freelancer_manager = FreelancerManager()

    def main(self):
        # Load data
        self.user_manager.load_users()
        self.freelancer_manager.load_freelancers()
        self.project_manager.load_projects()
        # Start application logic (e.g., render login page)
        self.render_login()

    def render_login(self):
        print("Rendering login page...")  # Placeholder for actual HTML rendering

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append((username, password))

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user[0]}|{user[1]}\n")

class ProjectManager:
    def __init__(self):
        self.projects = []

    def load_projects(self):
        if os.path.exists('projects.txt'):
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, freelancer = line.strip().split('|')
                    self.projects.append((name, description, freelancer))

    def create_project(self, name: str, description: str, freelancer: str) -> bool:
        self.projects.append((name, description, freelancer))
        self.save_projects()
        return True

    def list_projects(self) -> list:
        return self.projects

    def save_projects(self):
        with open('projects.txt', 'w') as file:
            for project in self.projects:
                file.write(f"{project[0]}|{project[1]}|{project[2]}\n")

class FreelancerManager:
    def __init__(self):
        self.freelancers = []

    def load_freelancers(self):
        if os.path.exists('freelancers.txt'):
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, details = line.strip().split('|')
                    self.freelancers.append((name, details))

    def search_freelancer(self, name: str) -> list:
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer[0].lower()]

    def get_freelancer_details(self, name: str) -> str:
        for freelancer in self.freelancers:
            if freelancer[0] == name:
                return freelancer[1]
        return "Freelancer not found."