from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users():
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass  # Handle case where the file does not exist
        return users

    @staticmethod
    def find_user(username: str):
        users = User.load_users()
        if username in users:
            return User(username, users[username])
        return None

class Freelancer:
    def __init__(self, name: str, skills: str):
        self.name = name
        self.skills = skills

    def save(self):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{self.name}|{self.skills}\n")

    @staticmethod
    def load_freelancers():
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, skills = line.strip().split('|')
                    freelancers.append(Freelancer(name, skills))
        except FileNotFoundError:
            pass  # Handle case where the file does not exist
        return freelancers

    @staticmethod
    def find_freelancer(name: str):
        freelancers = Freelancer.load_freelancers()
        for freelancer in freelancers:
            if freelancer.name == name:
                return freelancer
        return None

    @staticmethod
    def search_freelancers_by_skill(skill: str):
        freelancers = Freelancer.load_freelancers()
        return [freelancer for freelancer in freelancers if skill.lower() in freelancer.skills.lower()]

class Project:
    def __init__(self, name: str, description: str, assigned_freelancer: str):
        self.name = name
        self.description = description
        self.assigned_freelancer = assigned_freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.assigned_freelancer}\n")

    @staticmethod
    def load_projects():
        projects = []
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, assigned_freelancer = line.strip().split('|')
                    projects.append(Project(name, description, assigned_freelancer))
        except FileNotFoundError:
            pass  # Handle case where the file does not exist
        return projects

    @staticmethod
    def find_project(name: str):
        projects = Project.load_projects()
        for project in projects:
            if project.name == name:
                return project
        return None

class Application:
    def __init__(self):
        self.users = User.load_users()
        self.freelancers = Freelancer.load_freelancers()
        self.projects = Project.load_projects()

    def register_user(self, username: str, password: str):
        if username in self.users:
            return False
        user = User(username, password)
        user.save()
        self.users[username] = password
        return True

    def login(self, username: str, password: str):
        user = User.find_user(username)
        if user and user.password == password:
            return True
        return False

    def search_freelancer(self, name: str):
        return Freelancer.find_freelancer(name)

    def search_freelancers_by_skill(self, skill: str):
        return Freelancer.search_freelancers_by_skill(skill)

    def create_project(self, name: str, description: str, freelancer: str):
        project = Project(name, description, freelancer)
        project.save()
        self.projects.append(project)

    def update_profile(self, username: str, new_username: str, new_password: str):
        users = User.load_users()
        if username in users:
            del users[username]
            new_user = User(new_username, new_password)
            new_user.save()
            return True
        return False

    def view_freelancer_profile(self, name: str):
        return Freelancer.find_freelancer(name)

    def view_projects(self):
        return Project.load_projects()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = Application()
        if app_instance.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        app_instance = Application()
        if app_instance.register_user(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/manage_projects', methods=['GET', 'POST'])
def project_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    app_instance = Application()
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        assigned_freelancer = request.form['assigned_freelancer']
        app_instance.create_project(project_name, project_description, assigned_freelancer)
        return redirect(url_for('project_management'))
    freelancers = app_instance.freelancers
    return render_template('project_management.html', freelancers=freelancers)

@app.route('/search_freelancers', methods=['GET', 'POST'])
def search_freelancers():
    if 'username' not in session:
        return redirect(url_for('login'))
    app_instance = Application()
    if request.method == 'POST':
        skill = request.form['skill']
        freelancers = app_instance.search_freelancers_by_skill(skill)
        return render_template('search_results.html', freelancers=freelancers)
    return render_template('search_freelancers.html')

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    app_instance = Application()
    if request.method == 'POST':
        username = session['username']
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        if app_instance.update_profile(username, new_username, new_password):
            session['username'] = new_username
            return redirect(url_for('home'))
    return render_template('update_profile.html')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    if 'username' not in session:
        return redirect(url_for('login'))
    app_instance = Application()
    freelancer = app_instance.view_freelancer_profile(name)
    if freelancer:
        return render_template('freelancer_profile.html', freelancer=freelancer)
    return "Freelancer not found", 404

@app.route('/projects')
def view_projects():
    if 'username' not in session:
        return redirect(url_for('login'))
    app_instance = Application()
    projects = app_instance.view_projects()
    return render_template('projects.html', projects=projects)

if __name__ == '__main__':
    app.run(port=8369, debug=False)
