from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/project_management')
def project_management():
    return render_template('project_management.html')

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8302, debug=False)
