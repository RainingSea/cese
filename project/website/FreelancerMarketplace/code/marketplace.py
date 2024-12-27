from user import User
from freelancer import Freelancer
from project import Project

class Marketplace:
    def __init__(self):
        self.users = []
        self.freelancers = []
        self.projects = []
        self.load_users()
        self.load_freelancers()
        self.load_projects()

    def load_users(self):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if len(user_data) == 2:
                    self.users.append(User(user_data[0], user_data[1]))

    def load_freelancers(self):
        with open('freelancers.txt', 'r') as file:
            for line in file:
                freelancer_data = line.strip().split('|')
                if len(freelancer_data) >= 2:
                    name = freelancer_data[0]
                    skills = freelancer_data[1].split(',')
                    self.freelancers.append(Freelancer(name, skills))

    def load_projects(self):
        with open('projects.txt', 'r') as file:
            for line in file:
                project_data = line.strip().split('|')
                if len(project_data) == 3:
                    self.projects.append(Project(project_data[0], project_data[1], project_data[2]))

    def register_user(self, username: str, password: str):
        if self.load_user(username) is None:
            new_user = User(username, password)
            new_user.save()
            self.users.append(new_user)

    def load_user(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def login(self, username: str, password: str) -> bool:
        user = self.load_user(username)
        if user and user.password == password:
            return True
        return False

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer.name.lower()]

    def create_project(self, name: str, description: str, freelancer: str):
        new_project = Project(name, description, freelancer)
        new_project.save()
        self.projects.append(new_project)