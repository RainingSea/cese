from flask import Flask, render_template, request, redirect, session
from data_manager import DataManager
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
data_manager = DataManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/home')
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        data_manager.save_user(new_user)
        return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        new_project = Project(project_name, description, freelancer)
        data_manager.save_project(new_project)
        return redirect('/home')
    return render_template('project_management.html')

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Update user logic can go here
        return redirect('/home')
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8092, debug=False)
