from flask import Flask, render_template, request, redirect, url_for, session
import json

class UserManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.users, file)

class ProjectManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.projects = self.load_projects()

    def create_project(self, name: str, description: str, freelancer: str) -> bool:
        self.projects.append({"name": name, "description": description, "freelancer": freelancer})
        self.save_projects()
        return True

    def load_projects(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_projects(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.projects, file)

class FreelancerManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.freelancers = self.load_freelancers()

    def add_freelancer(self, name: str, details: str) -> bool:
        self.freelancers.append({"name": name, "details": details})
        self.save_freelancers()
        return True

    def load_freelancers(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_freelancers(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.freelancers, file)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
project_manager = ProjectManager('projects.txt')
freelancer_manager = FreelancerManager('freelancers.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Handle profile update logic
        pass
    return render_template('profile.html')

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project_manager.create_project(name, description, freelancer)
    return render_template('project_management.html')

@app.route('/freelancer_profile/<name>', methods=['GET'])
def freelancer_profile(name):
    freelancer = next((f for f in freelancer_manager.freelancers if f['name'] == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

if __name__ == '__main__':
    app.run(port=8167, debug=False)
