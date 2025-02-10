from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from project_manager import ProjectManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager()
project_manager = ProjectManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.find_user(username) and user_manager.find_user(username).password == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager.add_user(User(username, password, email))
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer/<username>')
def freelancer_profile(username):
    user = user_manager.find_user(username)
    return render_template('freelancer_profile.html', user=user)

@app.route('/manage_projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        assigned_freelancer = request.form['assigned_freelancer']
        project_manager.add_project(Project(name, description, assigned_freelancer))
    projects = project_manager.get_projects()
    return render_template('manage_projects.html', projects=projects)

@app.route('/profile_management')
def profile_management():
    return render_template('profile_management.html')

if __name__ == '__main__':
    user_manager.load_users()
    project_manager.load_projects()
    app.run(port=8538, debug=False)
