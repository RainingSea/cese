from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from resource import Resource
from message import Message
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_file_users = 'users.txt'
data_file_resources = 'resources.txt'
data_file_messages = 'messages.txt'

class SocialLearnApp:
    def __init__(self):
        self.users = []
        self.resources = []
        self.messages = []
        self.load_data()

    def load_data(self):
        if os.path.exists(data_file_users):
            with open(data_file_users, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        
        if os.path.exists(data_file_resources):
            with open(data_file_resources, 'r') as file:
                for line in file:
                    title, link = line.strip().split('|')
                    self.resources.append(Resource(title, link))
        
        if os.path.exists(data_file_messages):
            with open(data_file_messages, 'r') as file:
                for line in file:
                    sender, receiver, content = line.strip().split('|')
                    self.messages.append(Message(sender, receiver, content))

    def save_data(self):
        with open(data_file_users, 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")
        
        with open(data_file_resources, 'w') as file:
            for resource in self.resources:
                file.write(f"{resource.title}|{resource.link}\n")
        
        with open(data_file_messages, 'w') as file:
            for message in self.messages:
                file.write(f"{message.sender}|{message.receiver}|{message.content}\n")
    
    def register_user(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_data()
    
    def login_user(self, username: str, password: str):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False
    
    def add_resource(self, title: str, link: str):
        new_resource = Resource(title, link)
        self.resources.append(new_resource)
        self.save_data()
    
    def send_message(self, sender: str, receiver: str, content: str):
        new_message = Message(sender, receiver, content)
        self.messages.append(new_message)
        self.save_data()

social_learn_app = SocialLearnApp()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if social_learn_app.login_user(username, password):
            session['username'] = username
            return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        social_learn_app.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/study_groups')
def study_groups():
    return render_template('study_groups.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        social_learn_app.add_resource(title, link)
    return render_template('resources.html', resources=social_learn_app.resources)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        sender = session.get('username')
        receiver = request.form['receiver']
        content = request.form['content']
        social_learn_app.send_message(sender, receiver, content)
    return render_template('messages.html', messages=social_learn_app.messages)

if __name__ == '__main__':
    app.run(port=8637, debug=False)
