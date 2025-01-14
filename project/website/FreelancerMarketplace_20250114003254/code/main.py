from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = User.load_all()
    return {user.username: user.password for user in users}

def load_freelancers():
    return Freelancer.load_all()

def load_projects():
    return Project.load_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
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

@app.route('/home', methods=['GET', 'POST'])
def home():
    freelancers = load_freelancers()
    if request.method == 'POST':
        search_query = request.form['search_query']
        freelancers = [freelancer for freelancer in freelancers if search_query.lower() in freelancer.name.lower()]
    return render_template('home.html', freelancers=freelancers)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        project = Project(name, description, freelancer)
        project.save()
    projects = load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        user = User(session['username'], '')
        user.update_profile(new_username, new_email)
        session['username'] = new_username  # Update session username
        return redirect(url_for('profile_management'))  # Redirect to avoid resubmission
    return render_template('profile_management.html')

@app.route('/freelancer/<string:name>', methods=['GET'])
def freelancer_profile(name):
    freelancers = load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    if freelancer:
        return render_template('freelancer_profile.html', freelancer=freelancer)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8457, debug=False)
