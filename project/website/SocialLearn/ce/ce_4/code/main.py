from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from profile import Profile
from resource import Resource
from message import Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_profiles():
    profiles = {}
    with open('profiles.txt', 'r') as file:
        for line in file:
            username, interests = line.strip().split('|')
            profiles[username] = interests.split(',')
    return profiles

@app.route('/')
def login():
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

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        interests = request.form['interests'].split(',')
        profile = Profile(session['username'], interests)
        profile.save()
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/login', methods=['POST'])
def do_login():
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/study_groups')
def study_groups():
    return render_template('study_groups.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        resource = Resource(title, link)
        resource.save()
        return redirect(url_for('resources'))
    return render_template('resources.html')

@app.route('/messaging', methods=['GET', 'POST'])
def messaging():
    if request.method == 'POST':
        receiver = request.form['receiver']
        content = request.form['content']
        message = Message(session['username'], receiver, content)
        message.save()
        return redirect(url_for('messaging'))
    return render_template('messaging.html')

if __name__ == '__main__':
    app.run(port=8639, debug=False)
