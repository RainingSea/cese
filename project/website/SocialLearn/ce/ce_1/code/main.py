from flask import Flask, render_template, request, redirect, session, flash
from user import User
from profile import Profile
from study_group import StudyGroup
from resource import Resource
from message import Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def load_profiles():
    profiles = {}
    if os.path.exists('profiles.txt'):
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
        users = load_users()
        if username in users:
            flash("Registration Failed: Username already exists.")
            return redirect('/register')
        else:
            new_user = User(username, password)
            new_user.save()
            flash("Registration successful! Please log in.")
            return redirect('/')
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/profile')
        flash("Login Failed: Invalid username or password.")
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    profiles = load_profiles()
    if request.method == 'POST':
        interests = request.form['interests'].split(',')
        profile = Profile(username)
        profile.update(interests)
    return render_template('profile.html', username=username, interests=profiles.get(username, []))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8317, debug=False)
