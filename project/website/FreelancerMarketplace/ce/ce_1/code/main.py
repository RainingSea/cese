from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import User, Project, Freelancer

app = Flask(__name__)
data_manager = DataManager('users.txt', 'projects.txt', 'freelancers.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        data_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project = Project(name, description, freelancer)
        data_manager.save_project(project)
        return redirect(url_for('projects'))
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(port=8537, debug=False)
