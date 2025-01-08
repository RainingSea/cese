from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

# Load freelancers from file
def load_freelancers():
    freelancers = []
    with open('freelancers.txt', 'r') as f:
        for line in f:
            name, details = line.strip().split('|')
            freelancers.append(Freelancer(name, details))
    return freelancers

# Load projects from file
def load_projects():
    projects = []
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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    freelancers = load_freelancers()
    return render_template('freelancer_profile.html', freelancers=freelancers)

@app.route('/project_management')
def project_management():
    projects = load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8299, debug=False)
