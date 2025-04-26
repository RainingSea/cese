from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.interests = []

    def createProfile(self, username: str, password: str, interests: List[str]) -> None:
        self.username = username
        self.password = password
        self.interests = interests

    def updateProfile(self, interests: List[str]) -> None:
        self.interests = interests

class StudyGroup:
    def __init__(self, groupName: str):
        self.groupName = groupName
        self.members = []

    def joinGroup(self, user: User) -> None:
        self.members.append(user)

class Resource:
    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link

    def shareResource(self, title: str, link: str) -> None:
        self.title = title
        self.link = link

class Message:
    def __init__(self, sender: str, content: str):
        self.sender = sender
        self.content = content

    def sendMessage(self, sender: str, content: str) -> None:
        self.sender = sender
        self.content = content

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Save user to users.txt
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect('/')
    return render_template('registration.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        # Update user profile logic
        return redirect('/profile')
    return render_template('profile.html')

@app.route('/study_groups')
def study_groups():
    # Load study groups from study_groups.txt
    return render_template('study_groups.html')

@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        # Save resource to resources.txt
        with open('resources.txt', 'a') as f:
            f.write(f"{title}|{link}\n")
        return redirect('/resources')
    return render_template('resources.html')

@app.route('/messaging', methods=['GET', 'POST'])
def messaging():
    if request.method == 'POST':
        sender = request.form['sender']
        content = request.form['content']
        # Save message to messages.txt
        with open('messages.txt', 'a') as f:
            f.write(f"{sender}|{content}\n")
        return redirect('/messaging')
    return render_template('messaging.html')

if __name__ == '__main__':
    app.run(port=8242, debug=False)
