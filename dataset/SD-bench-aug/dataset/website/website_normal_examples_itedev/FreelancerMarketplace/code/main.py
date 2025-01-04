from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load users from the text file
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

# Save users to the text file
def save_user(user):
    with open('users.txt', 'a') as file:
        file.write(f"{user.username}|{user.password}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        save_user(new_user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    freelancers = load_freelancers()
    search_results = []
    
    if request.method == 'POST':
        search_name = request.form['search_name']
        search_results = [freelancer for freelancer in freelancers if search_name.lower() in freelancer.name.lower()]
    
    return render_template('home.html', username=session['username'], freelancers=search_results)

# Load freelancers from the text file
def load_freelancers():
    freelancers = []
    if os.path.exists('freelancers.txt'):
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, skills = line.strip().split('|')
                skills_list = skills.split(',')
                freelancers.append(Freelancer(name, skills_list))
    return freelancers

@app.route('/freelancer/<name>', methods=['GET'])
def freelancer_profile(name):
    freelancers = load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    if freelancer is None:
        return "Freelancer not found.", 404
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if 'username' not in session:
        return redirect(url_for('login'))

    projects = load_projects()
    
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        freelancer_name = request.form['freelancer_name']
        new_project = Project(project_name, project_description, freelancer_name)
        new_project.save()
        return redirect(url_for('project_management'))

    return render_template('project_management.html', projects=projects)

# Load projects from the text file
def load_projects():
    projects = []
    if os.path.exists('projects.txt'):
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append(Project(name, description, freelancer))
    return projects

if __name__ == '__main__':
    app.run(debug=True)