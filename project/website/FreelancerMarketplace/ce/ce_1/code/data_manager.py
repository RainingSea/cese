from user import User
from freelancer import Freelancer
from project import Project

class DataManager:
    def save_user(self, user: User):
        user.save()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                users.append(User(user_data[0], user_data[1]))
        return users

    def save_freelancer(self, freelancer: Freelancer):
        freelancer.save()

    def load_freelancers(self):
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                freelancer_data = line.strip().split('|')
                skills = freelancer_data[1].split(',')
                freelancers.append(Freelancer(freelancer_data[0], skills))
        return freelancers

    def save_project(self, project: Project):
        project.save()

    def load_projects(self):
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                project_data = line.strip().split('|')
                projects.append(Project(project_data[0], project_data[1], project_data[2]))
        return projects