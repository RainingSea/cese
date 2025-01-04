from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load users from the users.txt file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

# Save users to the users.txt file
def save_user(user):
    with open('users.txt', 'a') as file:
        file.write(f"{user.username}|{user.password}\n")

# Load freelancers from the freelancers.txt file
def load_freelancers():
    freelancers = []
    try:
        with open('freelancers.txt', 'r') as file:
            for line in file:
                name, skills = line.strip().split('|')
                freelancers.append(Freelancer(name, skills.split(',')))
    except FileNotFoundError:
        pass
    return freelancers

# Save freelancer to the freelancers.txt file
def save_freelancer(freelancer):
    with open('freelancers.txt', 'a') as file:
        file.write(f"{freelancer.name}|{','.join(freelancer.skills)}\n")

# Load projects from the projects.txt file
def load_projects():
    projects = []
    try:
        with open('projects.txt', 'r') as file:
            for line in file:
                name, description, freelancer = line.strip().split('|')
                projects.append(Project(name, description, freelancer))
    except FileNotFoundError:
        pass
    return projects

# Save project to the projects.txt file
def save_project(project):
    with open('projects.txt', 'a') as file:
        file.write(f"{project.name}|{project.description}|{project.freelancer}\n")

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        # Check if username already exists
        if any(u.username == username for u in users):
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        new_user = User(username, password)
        save_user(new_user)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    
    return render_template('registration.html')

# User login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        # Check if the username and password match
        if any(u.username == username and u.password == password for u in users):
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password. Please try again.')
    
    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    freelancers = load_freelancers()
    search_query = request.args.get('search', '')
    if search_query:
        freelancers = [f for f in freelancers if search_query.lower() in f.name.lower()]
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancers = load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        freelancer_name = request.form['freelancer']
        new_project = Project(project_name, description, freelancer_name)
        save_project(new_project)
        flash('Project created successfully!')
        return redirect(url_for('project_management'))

    freelancers = load_freelancers()
    projects = load_projects()
    return render_template('project_management.html', freelancers=freelancers, projects=projects)

if __name__ == '__main__':
    app.run(debug=True)