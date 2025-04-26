from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

class FreelancerManager:
    def __init__(self):
        self.freelancers = self.load_freelancers()

    def load_freelancers(self):
        if not os.path.exists('freelancers.txt'):
            return []
        with open('freelancers.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def search_freelancer(self, name: str) -> list:
        return [freelancer for freelancer in self.freelancers if name.lower() in freelancer[0].lower()]

    def get_freelancer_details(self, id: int) -> str:
        if 0 <= id < len(self.freelancers):
            return '|'.join(self.freelancers[id])
        return "Freelancer not found."

class ProjectManager:
    def __init__(self):
        self.projects = self.load_projects()

    def load_projects(self):
        if not os.path.exists('projects.txt'):
            return []
        with open('projects.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def create_project(self, name: str, description: str, freelancer_id: int) -> bool:
        self.projects.append([name, description, str(freelancer_id)])
        with open('projects.txt', 'a') as file:
            file.write(f"{name}|{description}|{freelancer_id}\n")
        return True

    def list_projects(self) -> list:
        return self.projects

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager = UserManager()
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. User may already exist."
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freelancer_profile/<int:id>')
def freelancer_profile(id):
    freelancer_manager = FreelancerManager()
    details = freelancer_manager.get_freelancer_details(id)
    return render_template('freelancer_profile.html', details=details)

@app.route('/project_management', methods=['GET', 'POST'])
def project_management():
    project_manager = ProjectManager()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer_id = request.form['freelancer_id']
        project_manager.create_project(name, description, freelancer_id)
    projects = project_manager.list_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        # Logic for updating user profile
        pass
    return render_template('profile_management.html')

if __name__ == '__main__':
    app.run(port=8169, debug=False)
