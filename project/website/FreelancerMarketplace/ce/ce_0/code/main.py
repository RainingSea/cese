from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if any(user['username'] == username for user in users):
            return False
        users.append({'username': username, 'password': password})
        self.save_users(users)
        return True

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        return users

    def save_users(self, users):
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user['username']}|{user['password']}\n")

class Freelancer:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    def viewProfile(self) -> str:
        return f"Name: {self.name}, Info: {self.info}"

class Project:
    def __init__(self, name, description, assignedFreelancer=None):
        self.name = name
        self.description = description
        self.assignedFreelancer = assignedFreelancer

    def createProject(self, name: str, description: str, freelancer: Freelancer) -> bool:
        projects = self.load_projects()
        projects.append({'name': name, 'description': description, 'assignedFreelancer': freelancer.name})
        self.save_projects(projects)
        return True

    def viewProjects(self) -> list:
        return self.load_projects()

    def load_projects(self):
        projects = []
        if os.path.exists('projects.txt'):
            with open('projects.txt', 'r') as f:
                for line in f:
                    name, description, assignedFreelancer = line.strip().split('|')
                    projects.append({'name': name, 'description': description, 'assignedFreelancer': assignedFreelancer})
        return projects

    def save_projects(self, projects):
        with open('projects.txt', 'w') as f:
            for project in projects:
                f.write(f"{project['name']}|{project['description']}|{project['assignedFreelancer']}\n")

class Main:
    def __init__(self):
        self.user = User("", "")
        self.freelancer = Freelancer("", "")
        self.project = Project("", "")

    def main(self) -> str:
        return "Freelancer Marketplace Application"

    def searchFreelancer(self, query: str) -> list:
        freelancers = self.load_freelancers()
        return [f for f in freelancers if query.lower() in f['name'].lower()]

    def load_freelancers(self):
        freelancers = []
        if os.path.exists('freelancers.txt'):
            with open('freelancers.txt', 'r') as f:
                for line in f:
                    name, info = line.strip().split('|')
                    freelancers.append({'name': name, 'info': info})
        return freelancers

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            return render_template('home.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=8382, debug=False)
