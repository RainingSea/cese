import json
from User import User
from Project import Project
from Freelancer import Freelancer

class DataManager:
    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}|{user.email}\n")

    def load_projects(self) -> list:
        projects = []
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, freelancer = line.strip().split('|')
                    projects.append(Project(name, description, freelancer))
        except FileNotFoundError:
            pass
        return projects

    def save_project(self, project: Project):
        with open('projects.txt', 'a') as file:
            file.write(f"{project.name}|{project.description}|{project.freelancer}\n")

    def load_freelancers(self) -> list:
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, skills = line.strip().split('|')
                    freelancers.append(Freelancer(name, skills.split(',')))
        except FileNotFoundError:
            pass
        return freelancers

    def save_freelancer(self, freelancer: Freelancer):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{freelancer.name}|{','.join(freelancer.skills)}\n")