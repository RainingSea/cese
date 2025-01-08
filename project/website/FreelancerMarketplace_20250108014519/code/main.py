from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_freelancers():
    freelancers = []
    with open('freelancers.txt', 'r') as file:
        for line in file:
            name, details = line.strip().split('|')
            freelancers.append(Freelancer(name, details))
    return freelancers

def load_projects():
    projects = []
    with open('projects.txt', 'r') as file:
        for line in file:
            name, description, freelancer = line.strip().split('|')
            projects.append(Project(name, description, freelancer))
    return projects

users = load_users()
freelancers = load_freelancers()
projects = load_projects()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    for freelancer in freelancers:
        if freelancer.name == name:
            return render_template('freelancer_profile.html', freelancer=freelancer)
    return redirect(url_for('home'))

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        new_project = Project(name, description, freelancer)
        projects.append(new_project)
        new_project.save()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        new_username = request.form['new_username']
        for user in users:
            if user.username == session['username']:
                user.username = new_username
                user.save()
                session['username'] = new_username
                break
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8304, debug=False)
