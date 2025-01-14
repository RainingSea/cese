from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all():
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def update(username: str, new_password: str):
        users = User.load_all()
        with open('users.txt', 'w') as file:
            for user in users:
                if user.username == username:
                    user.password = new_password
                file.write(f"{user.username}|{user.password}\n")

class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load_all():
        freelancers = []
        try:
            with open('freelancers.txt', 'r') as file:
                for line in file:
                    name, details = line.strip().split('|')
                    freelancers.append(Freelancer(name, details))
        except FileNotFoundError:
            pass
        return freelancers

class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def save(self):
        with open('projects.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.freelancer}\n")

    @staticmethod
    def load_all():
        projects = []
        try:
            with open('projects.txt', 'r') as file:
                for line in file:
                    name, description, freelancer = line.strip().split('|')
                    projects.append(Project(name, description, freelancer))
        except FileNotFoundError:
            pass
        return projects

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    freelancers = Freelancer.load_all()
    return render_template('freelancer_profile.html', freelancers=freelancers)

@app.route('/project_management')
def project_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    projects = Project.load_all()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = User.load_all()
    return render_template('profile_management.html', users=users)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    new_password = request.form['new_password']
    User.update(session['username'], new_password)
    return redirect(url_for('profile_management'))

if __name__ == '__main__':
    app.run(port=8467, debug=False)
