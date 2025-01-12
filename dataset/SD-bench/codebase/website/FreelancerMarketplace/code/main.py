from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from project import Project
from freelancer import Freelancer

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class App:
    def __init__(self):
        self.users = self.load_users()
        self.projects = self.load_projects()
        self.freelancers = self.load_freelancers()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def load_projects(self):
        projects = []
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append(Project(name, description, freelancer))
        return projects

    def load_freelancers(self):
        freelancers = []
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, details = line.strip().split('|')
                freelancers.append(Freelancer(name, details))
        return freelancers

    def register_user(self, username: str, password: str, email: str):
        new_user = User(username, password, email)
        self.users.append(new_user)
        new_user.save()

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def create_project(self, name: str, description: str, freelancer: str):
        new_project = Project(name, description, freelancer)
        self.projects.append(new_project)
        new_project.save()

    def search_freelancer(self, name: str):
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer.name.lower()]

app_instance = App()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login_user(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        app_instance.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        freelancer_name = request.form['freelancer_name']
        app_instance.create_project(project_name, project_description, freelancer_name)
        return redirect(url_for('home'))
    return render_template('manage_projects.html', projects=app_instance.projects)

@app.route('/freelancers', methods=['GET'])
def view_freelancers():
    return render_template('freelancers.html', freelancers=app_instance.freelancers)

if __name__ == "__main__":
    app.run(port=8306, debug=False)
