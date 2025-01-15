from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all():
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    @staticmethod
    def update(username: str, new_password: str):
        users = User.load_all()
        with open('users.txt', 'w') as f:
            for user in users:
                if user.username == username:
                    user.password = new_password
                f.write(f"{user.username}|{user.password}\n")

class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def save(self):
        with open('freelancers.txt', 'a') as f:
            f.write(f"{self.name}|{self.details}\n")

    @staticmethod
    def load_all():
        freelancers = []
        if os.path.exists('freelancers.txt'):
            with open('freelancers.txt', 'r') as f:
                for line in f:
                    name, details = line.strip().split('|')
                    freelancers.append(Freelancer(name, details))
        return freelancers

    @staticmethod
    def search(query: str):
        freelancers = Freelancer.load_all()
        return [freelancer for freelancer in freelancers if query.lower() in freelancer.name.lower()]

    @staticmethod
    def get_details(name: str):
        freelancers = Freelancer.load_all()
        for freelancer in freelancers:
            if freelancer.name == name:
                return freelancer
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
    def load_all():
        projects = []
        if os.path.exists('projects.txt'):
            with open('projects.txt', 'r') as f:
                for line in f:
                    name, description, freelancer = line.strip().split('|')
                    projects.append(Project(name, description, freelancer))
        return projects

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('project_management'))
    return render_template('home.html')

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        freelancer_name = request.form['freelancer_name']
        project = Project(project_name, project_description, freelancer_name)
        project.save()
        return redirect(url_for('project_management'))
    
    projects = Project.load_all()
    freelancers = Freelancer.load_all()
    return render_template('project_management.html', projects=projects, freelancers=freelancers)

@app.route('/freelancer_profile', methods=['GET', 'POST'])
def freelancer_profile():
    if request.method == 'POST':
        query = request.form['search_query']
        freelancers = Freelancer.search(query)
    else:
        freelancers = Freelancer.load_all()
    return render_template('freelancer_profile.html', freelancers=freelancers)

@app.route('/freelancer/<name>', methods=['GET'])
def freelancer_detail(name):
    freelancer = Freelancer.get_details(name)
    return render_template('freelancer_detail.html', freelancer=freelancer)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        new_password = request.form['password']
        username = session.get('username')
        User.update(username, new_password)
        return redirect(url_for('home'))
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8534, debug=False)
