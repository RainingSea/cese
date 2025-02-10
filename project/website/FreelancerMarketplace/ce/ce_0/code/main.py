from flask import Flask, render_template, request, redirect, session
from user import User
from freelancer import Freelancer
from project import Project
from marketplace import Marketplace

app = Flask(__name__)
app.secret_key = 'your_secret_key'
marketplace = Marketplace('users.txt', 'freelancers.txt', 'projects.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    users = marketplace.load_users()
    
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return render_template('home.html', username=username)
    return redirect('/')

@app.route('/freelancer/<name>')
def freelancer_profile(name):
    freelancers = marketplace.load_freelancers()
    freelancer = next((f for f in freelancers if f.name == name), None)
    return render_template('freelancer_profile.html', freelancer=freelancer)

@app.route('/projects')
def project_management():
    projects = marketplace.load_projects()
    return render_template('project_management.html', projects=projects)

@app.route('/profile')
def profile_management():
    return render_template('profile_management.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(port=8536, debug=False)
