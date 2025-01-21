from flask import Flask, render_template, request, redirect, session
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
    def load(username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None

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
        with open('projects.txt', 'r') as file:
            for line in file:
                project_data = line.strip().split('|')
                projects.append(Project(project_data[0], project_data[1], project_data[2]))
        return projects

class Freelancer:
    def __init__(self, name: str, info: str):
        self.name = name
        self.info = info

    def save(self):
        with open('freelancers.txt', 'a') as file:
            file.write(f"{self.name}|{self.info}\n")

    @staticmethod
    def load_all():
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                freelancer_data = line.strip().split('|')
                freelancers.append(Freelancer(freelancer_data[0], freelancer_data[1]))
        return freelancers

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    freelancers = Freelancer.load_all()
    return render_template('freelancer_profile.html', freelancers=freelancers)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        new_project = Project(name, description, freelancer)
        new_project.save()
        return redirect('/project_management')
    projects = Project.load_all()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8946, debug=False)
