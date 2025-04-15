from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from text files
def load_users():
    """Load users from users.txt."""
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_profiles():
    """Load user profiles from profiles.txt."""
    profiles = {}
    with open('profiles.txt', 'r') as file:
        for line in file:
            username, interests = line.strip().split('|')
            profiles[username] = interests.split(',')
    return profiles

def load_resources():
    """Load resources from resources.txt."""
    resources = []
    with open('resources.txt', 'r') as file:
        for line in file:
            title, link = line.strip().split('|')
            resources.append((title, link))
    return resources

def load_messages():
    """Load messages from messages.txt."""
    messages = []
    with open('messages.txt', 'r') as file:
        for line in file:
            sender, receiver, content = line.strip().split('|')
            messages.append((sender, receiver, content))
    return messages

def load_study_groups():
    """Load study groups from study_groups.txt."""
    study_groups = {}
    with open('study_groups.txt', 'r') as file:
        for line in file:
            name, members = line.strip().split('|')
            study_groups[name] = members.split(',')
    return study_groups

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
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        flash("Registration successful! Please log in.")
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    """Render the user dashboard."""
    if 'username' not in session:
        return redirect('/')
    
    profiles = load_profiles()
    resources = load_resources()
    return render_template('dashboard.html', username=session['username'], interests=profiles.get(session['username'], []), resources=resources)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Manage user profile updates."""
    if 'username' not in session:
        return redirect('/')
    
    profiles = load_profiles()
    if request.method == 'POST':
        interests = request.form['interests']
        # Update existing profile or create a new one
        profiles[session['username']] = interests.split(',')
        with open('profiles.txt', 'w') as file:
            for user, interest in profiles.items():
                file.write(f"{user}|{','.join(interest)}\n")
        flash("Profile updated successfully!")
    
    return render_template('profile.html', username=session['username'], interests=profiles.get(session['username'], []))

@app.route('/login', methods=['POST'])
def user_login():
    """Handle user login."""
    users = load_users()
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return redirect('/dashboard')
    else:
        flash("Login Failed: Invalid username or password.")
    return redirect('/')

@app.route('/logout')
def logout():
    """Log out the user."""
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect('/')

@app.route('/study_groups', methods=['GET', 'POST'])
def study_groups():
    """Render study groups and handle joining."""
    if 'username' not in session:
        return redirect('/')
    
    groups = load_study_groups()
    if request.method == 'POST':
        group_name = request.form['group_name']
        if group_name in groups:
            if session['username'] not in groups[group_name]:
                groups[group_name].append(session['username'])
                # Update the study_groups.txt file
                with open('study_groups.txt', 'w') as file:
                    for name, members in groups.items():
                        file.write(f"{name}|{','.join(members)}\n")
                flash(f"You have joined the {group_name} study group.")
            else:
                flash("You are already a member of this study group.")
        else:
            flash("Study group not found.")
    
    return render_template('study_groups.html', groups=groups)

@app.route('/group_messages/<group_name>', methods=['GET', 'POST'])
def group_messages(group_name):
    """Handle messaging within study groups."""
    if 'username' not in session:
        return redirect('/')
    
    messages = load_messages()
    if request.method == 'POST':
        content = request.form['content']
        messages.append((session['username'], group_name, content))
        # Save the message to messages.txt
        with open('messages.txt', 'a') as file:
            file.write(f"{session['username']}|{group_name}|{content}\n")
        flash("Message sent successfully!")
    
    group_messages = [msg for msg in messages if msg[1] == group_name]
    return render_template('group_messages.html', group_name=group_name, messages=group_messages)

@app.route('/resources')
def resources():
    """Render educational resources."""
    resources = load_resources()
    return render_template('resources.html', resources=resources)

@app.route('/resource_details/<resource_title>')
def resource_details(resource_title):
    """Render details of a specific educational resource."""
    resources = load_resources()
    resource = next((r for r in resources if r[0] == resource_title), None)
    if resource:
        return render_template('resource_details.html', title=resource[0], link=resource[1])
    else:
        flash("Resource not found.")
        return redirect('/resources')

if __name__ == '__main__':
    app.run(port=8319, debug=False)
