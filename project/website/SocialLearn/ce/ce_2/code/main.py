from flask import Flask, render_template, request, redirect, session, flash
from user import User
from profile import Profile
from resource import Resource
from message import Message
from study_group import StudyGroup

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users() -> dict:
    """Load users from the users.txt file."""
    users = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    except Exception as e:
        print(f"Error loading users: {e}")
    return users

def load_profiles() -> dict:
    """Load profiles from the profiles.txt file."""
    profiles = {}
    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                username, interests = line.strip().split('|')
                profiles[username] = interests.split(',')
    except Exception as e:
        print(f"Error loading profiles: {e}")
    return profiles

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/profile')
        flash("Login Failed: Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash("Registration Failed: Username already exists.")
            return redirect('/register')
        new_user = User(username, password)
        new_user.save_to_file()
        flash("Registration successful! Please log in.")
        return redirect('/')
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Display and update user profile."""
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    profiles = load_profiles()
    if request.method == 'POST':
        interests = request.form['interests'].split(',')
        profile = Profile(username)
        profile.update_profile(interests)
    return render_template('profile.html', username=username, interests=profiles.get(username, []))

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8318, debug=False)
