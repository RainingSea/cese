from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from marketplace import Marketplace
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'
marketplace = Marketplace()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        marketplace.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if marketplace.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    freelancers = []
    if request.method == 'POST':
        search_name = request.form['search_name']
        freelancers = marketplace.search_freelancer(search_name)
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>', methods=['GET'])
def freelancer_profile(name):
    freelancer = Freelancer.load(name)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_description = request.form['project_description']
        freelancer_name = request.form['freelancer_name']
        marketplace.create_project(project_name, project_description, freelancer_name)
        return redirect(url_for('project_management'))
    
    projects = marketplace.projects
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        username = session['username']
        new_username = request.form['username']
        # Update user profile
        user = marketplace.load_user(username)
        if user:
            user.username = new_username
            # Save updated user data
            with open('users.txt', 'w') as file:
                for u in marketplace.users:
                    file.write(f"{u.username}|{u.password}\n")
            session['username'] = new_username  # Update session username
            return redirect(url_for('home'))
    return render_template('profile_management.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)