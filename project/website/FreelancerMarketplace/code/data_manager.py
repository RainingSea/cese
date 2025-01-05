import json
from user import User
from freelancer import Freelancer
from project import Project

class DataManager:
    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save_freelancer(self, freelancer: Freelancer):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{freelancer.name}|{','.join(freelancer.skills)}\n")

    def load_freelancers(self):
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, skills = line.strip().split('|')
                    freelancers.append(Freelancer(name, skills.split(',')))
        except FileNotFoundError:
            pass
        return freelancers

    def save_project(self, project: Project):
        with open('projects.txt', 'a') as file:
            file.write(f"{project.name}|{project.description}|{project.freelancer}\n")

    def load_projects(self):
        projects = []
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, freelancer = line.strip().split('|')
                    projects.append(Project(name, description, freelancer))
        except FileNotFoundError:
            pass
        return projects