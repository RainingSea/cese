from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from profile import Profile
from study_group import StudyGroup
from resource import Resource
from message import Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from text files
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return [line.strip().split('|') for line in file.readlines()]

# Save data to text files
def save_data(filename, data):
    with open(filename, 'w') as file:
        for entry in data:
            file.write('|'.join(entry) + '\n')

# Initialize data
users = load_data('users.txt')
profiles = load_data('profiles.txt')
study_groups = load_data('study_groups.txt')
resources = load_data('resources.txt')
messages = load_data('messages.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        users.append([user.username, user.password])
        save_data('users.txt', users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        username = session['username']
        interests = request.form.getlist('interests')
        profile = Profile(username, interests)
        profiles.append([profile.username, ','.join(profile.interests)])
        save_data('profiles.txt', profiles)
        return redirect(url_for('profile'))
    return render_template('profile.html', username=session.get('username'))

@app.route('/study_groups', methods=['GET', 'POST'])
def study_groups_page():
    if request.method == 'POST':
        group_name = request.form['group_name']
        group = StudyGroup(group_name)
        group.members.append(session['username'])
        study_groups.append([group.name, ','.join(group.members)])
        save_data('study_groups.txt', study_groups)
    return render_template('study_groups.html', study_groups=study_groups)

@app.route('/resources', methods=['GET', 'POST'])
def resources_page():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        resource = Resource(title, link)
        resources.append([resource.title, resource.link])
        save_data('resources.txt', resources)
    return render_template('resources.html', resources=resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages_page():
    if request.method == 'POST':
        sender = session['username']
        receiver = request.form['receiver']
        content = request.form['content']
        message = Message(sender, receiver, content)
        messages.append([message.sender, message.receiver, message.content])
        save_data('messages.txt', messages)
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(port=8635, debug=False)
