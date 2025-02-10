from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from freelancer_manager import FreelancerManager
from project_manager import ProjectManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
freelancer_manager = FreelancerManager()
project_manager = ProjectManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.create_user(username, password)
        return redirect('/')
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.authenticate(username, password):
            session['username'] = username
            return render_template('home.html', freelancers=freelancer_manager.load_freelancers())
    return render_template('home.html')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancer = freelancer_manager.search_freelancer(name)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer_assigned = request.form['freelancer_assigned']
        project_manager.create_project(name, description, freelancer_assigned)
    projects = project_manager.load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8539, debug=False)
