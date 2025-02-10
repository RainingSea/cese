from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.interests = []

    def update_profile(self, interests: list):
        self.interests = interests

class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

class Message:
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content

class SocialLearn:
    def __init__(self):
        self.users = self.load_users()
        self.resources = self.load_resources()
        self.messages = self.load_messages()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_resources(self):
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as file:
                for line in file:
                    title, link = line.strip().split('|')
                    resources.append(Resource(title, link))
        return resources

    def load_messages(self):
        messages = []
        if os.path.exists('messages.txt'):
            with open('messages.txt', 'r') as file:
                for line in file:
                    sender, recipient, content = line.strip().split('|')
                    messages.append(Message(sender, recipient, content))
        return messages

    def register_user(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def add_resource(self, title: str, link: str):
        new_resource = Resource(title, link)
        self.resources.append(new_resource)
        with open('resources.txt', 'a') as file:
            file.write(f"{title}|{link}\n")

    def send_message(self, sender: str, recipient: str, content: str):
        new_message = Message(sender, recipient, content)
        self.messages.append(new_message)
        with open('messages.txt', 'a') as file:
            file.write(f"{sender}|{recipient}|{content}\n")

    def fetch_messages(self, user: str) -> list:
        return [msg for msg in self.messages if msg.recipient == user]

social_learn = SocialLearn()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        social_learn.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/study_groups')
def study_groups():
    return render_template('study_groups.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

if __name__ == '__main__':
    app.run(port=8638, debug=False)
