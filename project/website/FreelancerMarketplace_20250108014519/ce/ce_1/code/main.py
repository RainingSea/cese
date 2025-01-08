from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer_profile/<name>')
def freelancer_profile(name):
    freelancers = load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        freelancer_name = request.form['freelancer_name']
        new_project = Project(project_name, description, freelancer_name)
        new_project.save()
        return redirect(url_for('home'))
    return render_template('project_management.html')

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        user = next((u for u in load_users() if u.username == username), None)
        if user:
            user.update_profile(new_username, new_email)
        return redirect(url_for('home'))
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8300, debug=False)
