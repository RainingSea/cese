from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str, username: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date
        self.username = username

    def to_string(self) -> str:
        return f"{self.subject}|{self.details}|{self.preferred_date}|{self.username}"

class SupportMessage:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def to_string(self) -> str:
        return f"{self.name}|{self.email}|{self.message}"

class App:
    def __init__(self):
        self.users: List[User] = []
        self.requests: List[TutoringRequest] = []
        self.support_messages: List[SupportMessage] = []
        self.load_users()
        self.load_requests()
        self.load_support_messages()

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    self.users.append(User(username, password, email))

    def save_users(self) -> None:
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(user.to_string() + '\n')

    def load_requests(self) -> None:
        if os.path.exists('tutoring_requests.txt'):
            with open('tutoring_requests.txt', 'r') as f:
                for line in f:
                    subject, details, preferred_date, username = line.strip().split('|')
                    self.requests.append(TutoringRequest(subject, details, preferred_date, username))

    def save_requests(self) -> None:
        with open('tutoring_requests.txt', 'w') as f:
            for request in self.requests:
                f.write(request.to_string() + '\n')

    def load_support_messages(self) -> None:
        if os.path.exists('support_messages.txt'):
            with open('support_messages.txt', 'r') as f:
                for line in f:
                    name, email, message = line.strip().split('|')
                    self.support_messages.append(SupportMessage(name, email, message))

    def save_support_messages(self) -> None:
        with open('support_messages.txt', 'w') as f:
            for message in self.support_messages:
                f.write(message.to_string() + '\n')

    def register_user(self, username: str, password: str, email: str) -> None:
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.save_users()

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def request_tutoring(self, subject: str, details: str, preferred_date: str, username: str) -> None:
        new_request = TutoringRequest(subject, details, preferred_date, username)
        self.requests.append(new_request)
        self.save_requests()

    def contact_support(self, name: str, email: str, message: str) -> None:
        new_message = SupportMessage(name, email, message)
        self.support_messages.append(new_message)
        self.save_support_messages()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
peer_tutoring_app = App()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if peer_tutoring_app.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        peer_tutoring_app.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/profile')
def profile():
    user = next((u for u in peer_tutoring_app.users if u.username == session.get('username')), None)
    return render_template('profile.html', user=user)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        peer_tutoring_app.contact_support(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8720, debug=False)
