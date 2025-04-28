from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append((username, password))
        return users

    def login(self, username: str, password: str) -> bool:
        return any(user for user in self.users if user[0] == username and user[1] == password)

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))
        return True

class FreelancerManager:
    def __init__(self):
        self.freelancers = self.load_freelancers()

    def load_freelancers(self):
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, details = line.strip().split('|')
                freelancers.append((name, details))
        return freelancers

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer[0].lower()]

    def view_freelancer_details(self, name: str):
        for freelancer in self.freelancers:
            if freelancer[0] == name:
                return freelancer[1]
        return None

class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    def load_projects(self):
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                project_name, description, freelancer = line.strip().split('|')
                projects.append((project_name, description, freelancer))
        return projects

    def create_project(self, name: str, description: str, freelancer: str) -> bool:
        with open('projects.txt', 'a') as file:
            file.write(f"{name}|{description}|{freelancer}\n")
        self.projects.append((name, description, freelancer))
        return True

    def list_projects(self):
        return self.projects

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return render_template('home.html', freelancers=freelancer_manager.freelancers)
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    details = freelancer_manager.view_freelancer_details(name)
    return render_template('freelancer_profile.html', name=name, details=details)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project_manager.create_project(project_name, description, freelancer)
    projects = project_manager.list_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    user_manager = UserManager()
    freelancer_manager = FreelancerManager()
    project_manager = ProjectManager()
    app.run(port=8383, debug=False)
