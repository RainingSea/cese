from flask import Flask, render_template, request, redirect, url_for, session
import os

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
    def __init__(self, subject: str, details: str, date: str, userId: int):
        self.subject = subject
        self.details = details
        self.date = date
        self.userId = userId

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        return users

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        for user in self.users:
            if user.username == username:
                return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

class TutorManager:
    def __init__(self):
        self.tutors = self.load_tutors()

    def load_tutors(self):
        tutors = []
        if os.path.exists('tutors.txt'):
            with open('tutors.txt', 'r') as file:
                for line in file:
                    name, subject = line.strip().split('|')
                    tutors.append(Tutor(name, subject))
        return tutors

    def viewTutors(self):
        return self.tutors

class RequestManager:
    def __init__(self):
        self.requests = self.load_requests()

    def load_requests(self):
        requests = []
        if os.path.exists('requests.txt'):
            with open('requests.txt', 'r') as file:
                for line in file:
                    subject, details, date, userId = line.strip().split('|')
                    requests.append(Request(subject, details, date, int(userId)))
        return requests

    def requestTutoring(self, subject: str, details: str, date: str, userId: int) -> bool:
        new_request = Request(subject, details, date, userId)
        self.requests.append(new_request)
        with open('requests.txt', 'a') as file:
            file.write(f"{subject}|{details}|{date}|{userId}\n")
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
                file.write(f"{request.subject}|{request.details}|{request.date}|{request.userId}\n")

user_manager = UserManager()
tutor_manager = TutorManager()
request_manager = RequestManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    tutors = tutor_manager.viewTutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8219, debug=False)
