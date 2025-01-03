from flask import Flask, render_template, request, redirect, session
from user import User
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and projects from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')[:2]
            users.append(User(username, password))
    return users

def load_projects():
    projects = []
    with open('projects.txt', 'r') as file:
        for line in file:
            project_name, description, assigned_freelancer = line.strip().split('|')
            projects.append(Project(project_name, description, assigned_freelancer))
    return projects

users = load_users()
projects = load_projects()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()  # Save the user using the User class method
        users.append(new_user)
        return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return render_template('home.html', username=username, projects=projects)
    return render_template('home.html', username=session.get('username'), projects=projects)

@app.route('/search_freelancer', methods=['POST'])
def search_freelancer():
    search_name = request.form['search_name']
    filtered_freelancers = [user.username for user in users if search_name.lower() in user.username.lower()]
    return render_template('home.html', username=session.get('username'), projects=projects, freelancers=filtered_freelancers)

@app.route('/freelancer_profile/<username>')
def freelancer_profile(username):
    freelancer = next((user for user in users if user.username == username), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/manage_projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        assigned_freelancer = request.form['assigned_freelancer']
        new_project = Project(project_name, description, assigned_freelancer)
        new_project.save()  # Save the project using the Project class method
        projects.append(new_project)
        return redirect('/manage_projects')
    return render_template('manage_projects.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        new_username = request.form['username']
        # Update the user's username
        current_user = next((user for user in users if user.username == session.get('username')), None)
        if current_user:
            current_user.username = new_username
            # Update the users.txt file
            with open('users.txt', 'w') as file:
                for user in users:
                    file.write(f"{user.username}|{user.password}\n")
            session['username'] = new_username  # Update session username
            return render_template('profile_management.html', message="Profile updated successfully.")
    return render_template('profile_management.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8129, debug=True)
