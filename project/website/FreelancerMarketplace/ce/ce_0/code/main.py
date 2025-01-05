from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from project import Project

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['DEBUG'] = True

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
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def search_freelancer(self, name: str):
        # Dummy implementation as we don't have a freelancer database
        return []

    def create_project(self, name: str, description: str, freelancer: str):
        new_project = Project(name, description, freelancer)
        new_project.save()
        self.projects.append(new_project)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        application = App()
        if application.login(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        application = App()
        application.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/projects', methods=['GET', 'POST'])
def project_management():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        freelancer = request.form['freelancer']
        application = App()
        application.create_project(name, description, freelancer)
        return redirect(url_for('project_management'))
    return render_template('project_management.html')

@app.route('/freelancer_profile')
def freelancer_profile():
    return render_template('freelancer_profile.html')

if __name__ == '__main__':
    application = App()
    app.run(port=8023, debug=False)
