from user import User
from freelancer import Freelancer
from project import Project

class Marketplace:
    def __init__(self, users_file: str, freelancers_file: str, projects_file: str):
        self.users_file = users_file
        self.freelancers_file = freelancers_file
        self.projects_file = projects_file
        self.load_data()

    def load_data(self):
        """Loads data from the specified files."""
        self.users = {}
        self.freelancers = {}
        self.projects = {}
        
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.users[username] = User(username, password)

        with open(self.freelancers_file, 'r') as file:
            for line in file:
                name, skills = line.strip().split('|')
                self.freelancers[name] = Freelancer(name, skills.split(','))

        with open(self.projects_file, 'r') as file:
            for line in file:
                name, description, assigned_freelancer = line.strip().split('|')
                self.projects[name] = Project(name, description, assigned_freelancer)

    def register_user(self, username: str, password: str) -> bool:
        """Registers a new user."""
        if username not in self.users:
            user = User(username, password)
            user.save()
            self.users[username] = user
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Handles user login."""
        user = self.users.get(username)
        return user and user.validate_password(password)

    def search_freelancer(self, name: str):
        """Searches for freelancers by name."""
        results = []
        for freelancer in self.freelancers.values():
            if name.lower() in freelancer.name.lower():
                results.append(freelancer)
        return results

    def create_project(self, name: str, description: str, freelancer_name: str):
        """Creates a new project."""
        project = Project(name, description, freelancer_name)
        project.save()
        self.projects[name] = project

    def update_profile(self, username: str, new_username: str, new_email: str):
        """Updates user profile information."""
        if username in self.users:
            user = self.users.pop(username)
            user.username = new_username
            user.save()
            self.users[new_username] = user

    def get_all_projects(self):
        """Returns all projects."""
        return list(self.projects.values())