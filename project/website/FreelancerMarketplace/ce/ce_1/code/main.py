from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class Application:
    def __init__(self):
        self.users = self.load_users()
        self.freelancers = self.load_freelancers()
        self.projects = self.load_projects()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def load_freelancers(self):
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as f:
                for line in f:
                    name, details = line.strip().split('|')
                    freelancers.append(Freelancer(name, details))
        except FileNotFoundError:
            pass
        return freelancers

    def load_projects(self):
        projects = []
        try:
            with open('projects.txt', 'r') as f:
                for line in f:
                    name, description, assigned_freelancer = line.strip().split('|')
                    projects.append(Project(name, description, assigned_freelancer))
        except FileNotFoundError:
            pass
        return projects

    def register_user(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        new_user.save()

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def create_freelancer(self, name: str, details: str):
        new_freelancer = Freelancer(name, details)
        self.freelancers.append(new_freelancer)
        new_freelancer.save()

    def create_project(self, name: str, description: str, assigned_freelancer: str):
        new_project = Project(name, description, assigned_freelancer)
        self.projects.append(new_project)
        new_project.save()

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if freelancer.name == name]

app_instance = Application()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    return render_template('freelancer_profile.html')

@app.route('/project_management')
def project_management():
    return render_template('project_management.html')

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8368, debug=False)
