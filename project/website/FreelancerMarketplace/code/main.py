from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

class App:
    def __init__(self):
        self.users = User.load_all()
        self.projects = Project.load_all()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def search_freelancer(self, name: str):
        # Placeholder for searching freelancers
        return []

    def create_project(self, name: str, description: str, freelancer: str):
        new_project = Project(name, description, freelancer)
        new_project.save()
        self.projects.append(new_project)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    app_instance = App()
    if app_instance.login(username, password):
        return redirect(url_for('home'))
    return redirect(url_for('login_page'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    app_instance = App()
    if app_instance.register(username, password):
        return redirect(url_for('login_page'))
    return redirect(url_for('login_page'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/project_management', methods=['POST'])
def project_management():
    name = request.form['name']
    description = request.form['description']
    freelancer = request.form['freelancer']
    app_instance = App()
    app_instance.create_project(name, description, freelancer)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8025, debug=False)
