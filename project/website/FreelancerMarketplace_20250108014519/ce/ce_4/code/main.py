from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from text files
def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_freelancers():
    freelancers = []
    with open('freelancers.txt', 'r') as f:
        for line in f:
            name, details = line.strip().split('|')
            freelancers.append(Freelancer(name, details))
    return freelancers

def load_projects():
    projects = []
    with open('projects.txt', 'r') as f:
        for line in f:
            name, description, freelancer = line.strip().split('|')
            projects.append(Project(name, description, freelancer))
    return projects

users = load_users()
freelancers = load_freelancers()
projects = load_projects()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users.append(User(username, password))
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>', methods=['GET'])
def freelancer_profile(name):
    freelancer = next((f for f in freelancers if f.name == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        projects.append(Project(name, description, freelancer))
        with open('projects.txt', 'a') as f:
            f.write(f"{name}|{description}|{freelancer}\n")
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        # Update user profile logic can be added here
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8303, debug=False)
