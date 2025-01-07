from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

users = load_users()

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

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile_management.html')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    return render_template('freelancer_profile.html', name=name)

@app.route('/projects', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        freelancer_name = request.form['freelancer_name']
        new_project = Project(project_name, project_description, freelancer_name)
        new_project.save()
    return render_template('project_management.html')

if __name__ == '__main__':
    app.run(port=8299, debug=False)
