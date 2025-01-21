from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        with open('projects.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.freelancer}\n")

    @staticmethod
    def load(name: str):
        with open('projects.txt', 'r') as f:
            for line in f:
                project_data = line.strip().split('|')
                if project_data[0] == name:
                    return Project(project_data[0], project_data[1], project_data[2])
        return None

class Freelancer:
    def __init__(self, name: str, skills: list):
        self.name = name
        self.skills = skills

    def save(self):
        with open('freelancers.txt', 'a') as f:
            f.write(f"{self.name}|{','.join(self.skills)}\n")

    @staticmethod
    def load(name: str):
        with open('freelancers.txt', 'r') as f:
            for line in f:
                freelancer_data = line.strip().split('|')
                if freelancer_data[0] == name:
                    return Freelancer(freelancer_data[0], freelancer_data[1].split(','))
        return None

class App:
    def __init__(self):
        self.users = []
        self.projects = []
        self.freelancers = []

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def register(self, username: str, password: str, email: str) -> None:
        new_user = User(username, password, email)
        new_user.save()

    def search_freelancer(self, name: str) -> list:
        freelancers = []
        with open('freelancers.txt', 'r') as f:
            for line in f:
                freelancer_data = line.strip().split('|')
                if name.lower() in freelancer_data[0].lower():
                    freelancers.append(Freelancer(freelancer_data[0], freelancer_data[1].split(',')))
        return freelancers

    def create_project(self, name: str, description: str, freelancer: str) -> None:
        new_project = Project(name, description, freelancer)
        new_project.save()

    def update_profile(self, username: str, email: str) -> None:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    users.append(f"{username}|{user_data[1]}|{email}\n")
                else:
                    users.append(line)
        with open('users.txt', 'w') as f:
            f.writelines(users)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        app_instance.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancer = Freelancer.load(name)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        app_instance.create_project(name, description, freelancer)
        return redirect(url_for('home'))
    return render_template('project_management.html')

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = session['username']
        email = request.form['email']
        app_instance.update_profile(username, email)
        return redirect(url_for('home'))
    return render_template('profile_management.html')

if __name__ == '__main__':
    app_instance = App()
    app.run(port=8948, debug=False)
