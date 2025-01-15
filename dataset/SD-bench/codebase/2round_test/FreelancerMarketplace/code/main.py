from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from freelancer_manager import FreelancerManager
from project_manager import ProjectManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager()
freelancer_manager = FreelancerManager()
project_manager = ProjectManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/home')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer/<username>')
def freelancer_profile(username):
    freelancers = freelancer_manager.load_freelancers()
    freelancer = next((f for f in freelancers if f.name == username), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project_manager.create_project(name, description, freelancer)
        return redirect('/project_management')
    projects = project_manager.load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.update_user(username, password):
            return redirect('/profile_management')
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8069, debug=False)
