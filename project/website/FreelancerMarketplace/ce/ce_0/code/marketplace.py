from user import User
from freelancer import Freelancer
from project import Project

class Marketplace:
    def __init__(self, users_file: str, freelancers_file: str, projects_file: str):
        self.users_file = users_file
        self.freelancers_file = freelancers_file
        self.projects_file = projects_file

    def load_users(self):
        users = []
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def load_freelancers(self):
        freelancers = []
        with open(self.freelancers_file, 'r') as file:
            for line in file:
                name, details = line.strip().split('|')
                freelancers.append(Freelancer(name, details))
        return freelancers

    def load_projects(self):
        projects = []
        with open(self.projects_file, 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append(Project(name, description, freelancer))
        return projects

    def add_user(self, user: User):
        user.save()

    def add_freelancer(self, freelancer: Freelancer):
        freelancer.save()

    def add_project(self, project: Project):
        project.save()