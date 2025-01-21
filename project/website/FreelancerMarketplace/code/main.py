from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from freelancer import Freelancer
from project import Project
from marketplace import Marketplace

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Initialize the Marketplace with file paths
marketplace = Marketplace('users.txt', 'freelancers.txt', 'projects.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if marketplace.login(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if marketplace.register_user(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists."
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    """Displays the home page and handles freelancer search."""
    freelancers = []
    if request.method == 'POST':
        name = request.form['name']
        freelancers = marketplace.search_freelancer(name)
    return render_template('home.html', freelancers=freelancers)

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    """Displays the freelancer profile."""
    freelancer_info = marketplace.search_freelancer(name)
    if freelancer_info:
        return render_template('freelancer_profile.html', freelancer=freelancer_info[0])
    return "Freelancer not found."

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    """Handles project management functionalities."""
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        freelancer_name = request.form['freelancer_name']
        marketplace.create_project(project_name, description, freelancer_name)
        return redirect(url_for('project_management'))
    projects = marketplace.get_all_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    """Handles user profile management."""
    current_user = session.get('username')  # Get current user from session
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        if current_user:
            marketplace.update_profile(current_user, new_username, new_email)
            session['username'] = new_username  # Update session username
            return redirect(url_for('home'))
    return render_template('profile_management.html', current_user=current_user)

@app.route('/view_projects')
def view_projects():
    """Displays all projects."""
    projects = marketplace.get_all_projects()
    return render_template('view_projects.html', projects=projects)

if __name__ == '__main__':
    app.run(port=8949, debug=False)
