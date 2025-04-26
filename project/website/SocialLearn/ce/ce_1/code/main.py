from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def update_profile(self, username: str, interests: list) -> bool:
        for user in self.users:
            if user[0] == username:
                user.append(','.join(interests))
                self.save_users()
                return True
        return False

class GroupManager:
    def __init__(self):
        self.groups = self.load_groups()

    def load_groups(self):
        if not os.path.exists('groups.txt'):
            return []
        with open('groups.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]

    def join_group(self, username: str, group_name: str) -> bool:
        if group_name not in self.groups:
            self.groups.append(group_name)
            self.save_groups()
        return True

    def save_groups(self):
        with open('groups.txt', 'w') as f:
            for group in self.groups:
                f.write(group + '\n')

class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self):
        if not os.path.exists('resources.txt'):
            return []
        with open('resources.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]

    def share_resource(self, username: str, resource: str) -> bool:
        self.resources.append(f"{username}|{resource}")
        self.save_resources()
        return True

    def save_resources(self):
        with open('resources.txt', 'w') as f:
            for resource in self.resources:
                f.write(resource + '\n')

class MessageManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        if not os.path.exists('messages.txt'):
            return []
        with open('messages.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]

    def send_message(self, from_user: str, to_user: str, message: str) -> bool:
        self.messages.append(f"{from_user}|{to_user}|{message}")
        self.save_messages()
        return True

    def save_messages(self):
        with open('messages.txt', 'w') as f:
            for message in self.messages:
                f.write(message + '\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        user_manager.update_profile(session['username'], interests)
    return render_template('profile.html')

@app.route('/groups')
def groups():
    return render_template('groups.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        resource = request.form['resource']
        resource_manager.share_resource(session['username'], resource)
    return render_template('resources.html')

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        to_user = request.form['to_user']
        message = request.form['message']
        message_manager.send_message(session['username'], to_user, message)
    return render_template('messages.html')

if __name__ == '__main__':
    user_manager = UserManager()
    group_manager = GroupManager()
    resource_manager = ResourceManager()
    message_manager = MessageManager()
    app.run(port=8243, debug=False)
