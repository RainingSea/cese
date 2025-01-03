from flask import Flask, render_template, request, redirect, session
from user import User
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize users and projects lists
users = []
projects = []

def load_users():
    global users
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')[:2]
                users.append(User(username, password))
    except FileNotFoundError:
        pass

def load_projects():
    global projects
    try:
        with open('projects.txt', 'r') as file:
            for line in file:
                project_name, description, assigned_freelancer = line.strip().split('|')
                projects.append(Project(project_name, description, assigned_freelancer))
    except FileNotFoundError:
        pass

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        users.append(new_user)
        return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/manage_projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        assigned_freelancer = request.form['assigned_freelancer']
        new_project = Project(project_name, description, assigned_freelancer)
        new_project.save()
        projects.append(new_project)
        return redirect('/manage_projects')
    
    return render_template('manage_projects.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        new_username = request.form['username']
        current_user = User.load(session['username'])
        if current_user:
            current_user.username = new_username
            current_user.save()
            session['username'] = new_username
            return redirect('/home')
    return render_template('profile_management.html')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')
    filtered_freelancers = [user.username for user in users if search_query.lower() in user.username.lower()]
    return render_template('home.html', freelancers=filtered_freelancers)

@app.route('/freelancer_profile/<username>')
def freelancer_profile(username):
    user = User.load(username)
    if user:
        return render_template('freelancer_profile.html', freelancer=user)
    return redirect('/home')

if __name__ == '__main__':
    load_users()
    load_projects()
    app.run(port=8130, debug=True)
