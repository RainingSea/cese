from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                login_user(user)
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        return True

class FreelancerManager:
    def __init__(self):
        self.freelancers = []
        self.load_freelancers()

    def load_freelancers(self):
        if os.path.exists('freelancers.txt'):
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    self.freelancers.append(line.strip())

    def save_freelancers(self):
        with open('freelancers.txt', 'w') as file:
            for freelancer in self.freelancers:
                file.write(f"{freelancer}\n")

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer.lower()]

class ProjectManager:
    def __init__(self):
        self.projects = []
        self.load_projects()

    def load_projects(self):
        if os.path.exists('projects.txt'):
            with open('projects.txt', 'r') as file:
                for line in file:
                    self.projects.append(line.strip())

    def save_projects(self):
        with open('projects.txt', 'w') as file:
            for project in self.projects:
                file.write(f"{project}\n")

    def create_project(self, name: str, description: str, freelancer: str):
        self.projects.append(f"{name}|{description}|{freelancer}")
        self.save_projects()

user_manager = UserManager()
freelancer_manager = FreelancerManager()
project_manager = ProjectManager()

@login_manager.user_loader
def load_user(user_id):
    for user in user_manager.users:
        if user.username == user_id:
            return user
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('registration.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search_freelancer', methods=['GET'])
@login_required
def search_freelancer():
    name = request.args.get('name', '')
    results = freelancer_manager.search_freelancer(name)
    return render_template('freelancer_profile.html', results=results)

@app.route('/project_management', methods=['GET'])
@login_required
def project_management():
    projects = project_manager.projects
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
@login_required
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # Here you would normally update the user's profile
        flash('Profile updated successfully')
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8170, debug=False)

