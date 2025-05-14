from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class FileStorage:
    @staticmethod
    def read_users():
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    @staticmethod
    def write_user(username, password):
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    @staticmethod
    def read_profiles():
        profiles = {}
        if os.path.exists('profiles.txt'):
            with open('profiles.txt', 'r') as f:
                for line in f:
                    username, interests, expertise = line.strip().split('|')
                    profiles[username] = {'interests': interests, 'expertise': expertise}
        return profiles

    @staticmethod
    def write_profile(username, interests, expertise):
        with open('profiles.txt', 'a') as f:
            f.write(f"{username}|{interests}|{expertise}\n")
        return True

    @staticmethod
    def read_groups():
        groups = {}
        if os.path.exists('groups.txt'):
            with open('groups.txt', 'r') as f:
                for line in f:
                    name, description, members = line.strip().split('|')
                    groups[name] = {'description': description, 'members': members.split(',')}
        return groups

    @staticmethod
    def write_group(name, description, members):
        with open('groups.txt', 'a') as f:
            f.write(f"{name}|{description}|{','.join(members)}\n")
        return True

    @staticmethod
    def read_resources():
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as f:
                for line in f:
                    title, type_, url, uploader = line.strip().split('|')
                    resources.append({'title': title, 'type': type_, 'url': url, 'uploader': uploader})
        return resources

    @staticmethod
    def write_resource(title, type_, url, uploader):
        with open('resources.txt', 'a') as f:
            f.write(f"{title}|{type_}|{url}|{uploader}\n")
        return True

    @staticmethod
    def read_messages():
        messages = []
        if os.path.exists('messages.txt'):
            with open('messages.txt', 'r') as f:
                for line in f:
                    sender, receiver, group, content = line.strip().split('|')
                    messages.append({'sender': sender, 'receiver': receiver, 'group': group, 'content': content})
        return messages

    @staticmethod
    def write_message(sender, receiver, group, content):
        with open('messages.txt', 'a') as f:
            f.write(f"{sender}|{receiver}|{group}|{content}\n")
        return True

class SocialLearnApp:
    def __init__(self):
        self.current_user = None
        self.storage = FileStorage()

    def login(self, username, password):
        users = self.storage.read_users()
        if username in users and users[username] == password:
            self.current_user = username
            return True
        return False

    def register(self, username, password):
        users = self.storage.read_users()
        if username in users:
            return False
        self.storage.write_user(username, password)
        self.current_user = username
        return True

    def update_profile(self, interests, expertise):
        if not self.current_user:
            return False
        return self.storage.write_profile(self.current_user, interests, expertise)

    def join_group(self, group_name):
        if not self.current_user:
            return False
        groups = self.storage.read_groups()
        if group_name not in groups:
            return False
        if self.current_user not in groups[group_name]['members']:
            groups[group_name]['members'].append(self.current_user)
            with open('groups.txt', 'w') as f:
                for name, data in groups.items():
                    f.write(f"{name}|{data['description']}|{','.join(data['members'])}\n")
        return True

    def share_resource(self, title, type_, url):
        if not self.current_user:
            return False
        return self.storage.write_resource(title, type_, url, self.current_user)

    def send_message(self, receiver, group, content):
        if not self.current_user:
            return False
        return self.storage.write_message(self.current_user, receiver, group, content)

app_instance = SocialLearnApp()

@app.route('/')
def home():
    if app_instance.current_user:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.register(username, password):
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if not app_instance.current_user:
        return redirect(url_for('login'))
    profiles = app_instance.storage.read_profiles()
    profile = profiles.get(app_instance.current_user, {})
    groups = app_instance.storage.read_groups()
    return render_template('dashboard.html', profile=profile, groups=groups)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not app_instance.current_user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        interests = request.form['interests']
        expertise = request.form['expertise']
        app_instance.update_profile(interests, expertise)
        return redirect(url_for('dashboard'))
    profiles = app_instance.storage.read_profiles()
    profile = profiles.get(app_instance.current_user, {})
    return render_template('profile.html', profile=profile)

@app.route('/groups', methods=['GET', 'POST'])
def groups():
    if not app_instance.current_user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        group_name = request.form['group_name']
        app_instance.join_group(group_name)
    groups = app_instance.storage.read_groups()
    return render_template('groups.html', groups=groups)

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if not app_instance.current_user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        type_ = request.form['type']
        url = request.form['url']
        app_instance.share_resource(title, type_, url)
    resources = app_instance.storage.read_resources()
    return render_template('resources.html', resources=resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if not app_instance.current_user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        receiver = request.form['receiver']
        group = request.form['group']
        content = request.form['content']
        app_instance.send_message(receiver, group, content)
    messages = app_instance.storage.read_messages()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(port=8050, debug=False)
