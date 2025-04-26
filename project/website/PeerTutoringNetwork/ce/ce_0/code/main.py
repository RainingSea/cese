from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

class Request:
    def __init__(self, subject: str, details: str, date: str):
        self.subject = subject
        self.details = details
        self.date = date

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [User(*line.strip().split('|')) for line in file.readlines()]

    def register(self, username: str, password: str, email: str) -> bool:
        new_user = User(username, password, email)
        self.users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

class TutorManager:
    def __init__(self):
        self.tutors = self.load_tutors()

    def load_tutors(self):
        if not os.path.exists('tutors.txt'):
            return []
        with open('tutors.txt', 'r') as file:
            return [Tutor(*line.strip().split('|')) for line in file.readlines()]

    def getTutors(self):
        return self.tutors

class RequestManager:
    def __init__(self):
        self.requests = self.load_requests()

    def load_requests(self):
        if not os.path.exists('requests.txt'):
            return []
        with open('requests.txt', 'r') as file:
            return [Request(*line.strip().split('|')) for line in file.readlines()]

    def createRequest(self, subject: str, details: str, date: str) -> bool:
        new_request = Request(subject, details, date)
        self.requests.append(new_request)
        with open('requests.txt', 'a') as file:
            file.write(f"{subject}|{details}|{date}\n")
        return True

    def cancelRequest(self, requestId: int) -> bool:
        if 0 <= requestId < len(self.requests):
            del self.requests[requestId]
            self.save_requests()
            return True
        return False

    def save_requests(self):
        with open('requests.txt', 'w') as file:
            for request in self.requests:
                file.write(f"{request.subject}|{request.details}|{request.date}\n")

user_manager = UserManager()
tutor_manager = TutorManager()
request_manager = RequestManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    tutors = tutor_manager.getTutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_manager.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8218, debug=False)
