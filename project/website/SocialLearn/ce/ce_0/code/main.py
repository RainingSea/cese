from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, interests: str):
        self.username = username
        self.password = password
        self.interests = interests

class Resource:
    def __init__(self, title: str, url: str, description: str):
        self.title = title
        self.url = url
        self.description = description

class Message:
    def __init__(self, sender: str, receiver: str, message: str):
        self.sender = sender
        self.receiver = receiver
        self.message = message

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> List[User]:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, interests = line.strip().split(',')
                users.append(User(username, password, interests))
        return users

    def register(self, username: str, password: str, interests: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password, interests))
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username},{user.password},{user.interests}\n")

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def update_profile(self, username: str, interests: str) -> None:
        for user in self.users:
            if user.username == username:
                user.interests = interests
                self.save_users()
                break

class ResourceManager:
    def __init__(self):
        self.resources = self.load_resources()

    def load_resources(self) -> List[Resource]:
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                title, url, description = line.strip().split(',')
                resources.append(Resource(title, url, description))
        return resources

    def add_resource(self, title: str, url: str, description: str) -> None:
        self.resources.append(Resource(title, url, description))
        self.save_resources()

    def save_resources(self):
        with open('resources.txt', 'w') as file:
            for resource in self.resources:
                file.write(f"{resource.title},{resource.url},{resource.description}\n")

    def get_resources(self) -> List[Resource]:
        return self.resources

class MessagingManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self) -> List[Message]:
        messages = []
        with open('messages.txt', 'r') as file:
            for line in file:
                sender, receiver, message = line.strip().split(',')
                messages.append(Message(sender, receiver, message))
        return messages

    def send_message(self, sender: str, receiver: str, message: str) -> None:
        self.messages.append(Message(sender, receiver, message))
        self.save_messages()

    def save_messages(self):
        with open('messages.txt', 'w') as file:
            for message in self.messages:
                file.write(f"{message.sender},{message.receiver},{message.message}\n")

    def get_messages(self, user: str) -> List[Message]:
        return [msg for msg in self.messages if msg.receiver == user or msg.sender == user]

user_manager = UserManager()
resource_manager = ResourceManager()
messaging_manager = MessagingManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        interests = request.form['interests']
        if user_manager.register(username, password, interests):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        interests = request.form['interests']
        user_manager.update_profile(session['username'], interests)
    user = next(user for user in user_manager.users if user.username == session['username'])
    return render_template('profile.html', user=user)

@app.route('/resources')
def resources():
    all_resources = resource_manager.get_resources()
    return render_template('resources.html', resources=all_resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        receiver = request.form['receiver']
        message = request.form['message']
        messaging_manager.send_message(session['username'], receiver, message)
    user_messages = messaging_manager.get_messages(session['username'])
    return render_template('messages.html', messages=user_messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8414, debug=False)
