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
    except FileNotFoundError:
        flash("User data file not found.")
    return users

def load_profiles() -> dict:
    """Load user profiles from the profiles.txt file."""
    profiles = {}
    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                username, interests = line.strip().split('|')
                profiles[username] = interests.split(',')
    except FileNotFoundError:
        flash("Profile data file not found.")
    return profiles

@app.route('/')
def login():
    """Render the login page."""
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
        else:
            new_user = User(username, password)
            new_user.save_to_file()
            flash("Registration successful! Please log in.")
            return redirect('/')
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Render and handle user profile management."""
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    profiles = load_profiles()
    if request.method == 'POST':
        interests = request.form['interests'].split(',')
        profile = Profile(username, interests)
        profile.save()
        flash("Profile updated successfully!")
    return render_template('profile.html', username=username, interests=profiles.get(username, []))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8316, debug=False)
