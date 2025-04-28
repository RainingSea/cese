from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

    def add_user(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def authenticate(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

class ProjectManager:
    def __init__(self):
        self.projects = []
        self.load_projects()

    def load_projects(self):
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, freelancer = line.strip().split('|')
                    self.projects.append({'name': name, 'description': description, 'freelancer': freelancer})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist

    def save_projects(self):
        with open('projects.txt', 'w') as file:
            for project in self.projects:
                file.write(f"{project['name']}|{project['description']}|{project['freelancer']}\n")

    def add_project(self, name: str, description: str, freelancer: str) -> bool:
        self.projects.append({'name': name, 'description': description, 'freelancer': freelancer})
        self.save_projects()
        return True

    def list_projects(self) -> list:
        return self.projects

class FreelancerManager:
    def __init__(self):
        self.freelancers = []
        self.load_freelancers()

    def load_freelancers(self):
        try:
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, skills = line.strip().split('|')
                    self.freelancers.append({'name': name, 'skills': skills.split(',')})
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist

    def save_freelancers(self):
        with open('freelancers.txt', 'w') as file:
            for freelancer in self.freelancers:
                file.write(f"{freelancer['name']}|{','.join(freelancer['skills'])}\n")

    def get_freelancer_details(self, name: str) -> dict:
        for freelancer in self.freelancers:
            if freelancer['name'] == name:
                return freelancer
        return {}

app = Flask(__name__)
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
        if user_manager.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.add_user(username, password):
            return redirect(url_for('login'))
        return "User already exists"
    return render_template('registration.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancer = freelancer_manager.get_freelancer_details(name)
    if freelancer:
        return render_template('freelancer_profile.html', freelancer=freelancer)
    return "Freelancer not found", 404

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project_manager.add_project(name, description, freelancer)
    projects = project_manager.list_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # Update profile logic here
        # For now, we will just return a success message
        return "Profile updated successfully"
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8385, debug=False)
