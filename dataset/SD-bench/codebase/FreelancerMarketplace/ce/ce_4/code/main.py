from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users, freelancers, and projects from respective files
def load_data():
    users = User.load_users()
    freelancers = Freelancer.load_freelancers()
    projects = Project.load_projects()
    return users, freelancers, projects

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
    return render_template('register.html')

@app.route('/home')
def home():
    users, freelancers, projects = load_data()
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancers = Freelancer.load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project = Project(name, description, freelancer)
        project.save()
        return redirect(url_for('project_management'))
    projects = Project.load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8303, debug=False)
