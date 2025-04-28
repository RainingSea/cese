from flask import Flask, render_template, request, redirect, session
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append({'username': username, 'password': password})
        return users

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append({'username': username, 'password': password})
        return True

class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    def load_projects(self):
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append({'name': name, 'description': description, 'freelancer': freelancer})
        return projects

    def create_project(self, name: str, description: str, freelancer: str) -> bool:
        with open('projects.txt', 'a') as file:
            file.write(f"{name}|{description}|{freelancer}\n")
        self.projects.append({'name': name, 'description': description, 'freelancer': freelancer})
        return True

    def list_projects(self):
        return self.projects

class FreelancerManager:
    def __init__(self):
        self.freelancers = self.load_freelancers()

    def load_freelancers(self):
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, skills = line.strip().split('|')
                freelancers.append({'name': name, 'skills': skills})
        return freelancers

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer['name'].lower()]

    def get_freelancer_details(self, name: str):
        for freelancer in self.freelancers:
            if freelancer['name'] == name:
                return freelancer
        return None

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
project_manager = ProjectManager()
freelancer_manager = FreelancerManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        return "User already exists"
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/projects')
def projects():
    project_list = project_manager.list_projects()
    return render_template('projects.html', projects=project_list)

if __name__ == '__main__':
    app.run(port=8384, debug=False)
