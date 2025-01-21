from flask import Flask, render_template, request, redirect, url_for, session
from DataManager import DataManager
from User import User
from Project import Project
from Freelancer import Freelancer

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        data_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return render_template('home.html', username=username)
    return render_template('login.html')

@app.route('/search_freelancer', methods=['POST'])
def search_freelancer():
    name = request.form['name']
    freelancers = data_manager.load_freelancers()
    results = [freelancer for freelancer in freelancers if name.lower() in freelancer.name.lower()]
    return render_template('home.html', freelancers=results)

@app.route('/create_project', methods=['POST'])
def create_project():
    name = request.form['name']
    description = request.form['description']
    freelancer = request.form['freelancer']
    project = Project(name, description, freelancer)
    data_manager.save_project(project)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8947, debug=False)
