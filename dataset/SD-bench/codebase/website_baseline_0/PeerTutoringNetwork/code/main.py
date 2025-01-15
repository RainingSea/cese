from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def to_string(self) -> str:
        return f"{self.subject}|{self.details}|{self.preferred_date}"

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def to_string(self) -> str:
        return f"{self.name}|{self.subject}"

class PeerTutoringNetwork:
    def __init__(self):
        self.users: List[User] = []
        self.tutoring_requests: List[TutoringRequest] = []
        self.tutors: List[Tutor] = []
        self.load_users()
        self.load_tutoring_requests()
        self.load_tutors()

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users.append(User(username, password, email))

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(user.to_string() + '\n')

    def load_tutoring_requests(self) -> None:
        if os.path.exists('tutoring_requests.txt'):
            with open('tutoring_requests.txt', 'r') as file:
                for line in file:
                    subject, details, preferred_date = line.strip().split('|')
                    self.tutoring_requests.append(TutoringRequest(subject, details, preferred_date))

    def save_tutoring_requests(self) -> None:
        with open('tutoring_requests.txt', 'w') as file:
            for request in self.tutoring_requests:
                file.write(request.to_string() + '\n')

    def load_tutors(self) -> None:
        if os.path.exists('tutors.txt'):
            with open('tutors.txt', 'r') as file:
                for line in file:
                    name, subject = line.strip().split('|')
                    self.tutors.append(Tutor(name, subject))

    def save_tutors(self) -> None:
        with open('tutors.txt', 'w') as file:
            for tutor in self.tutors:
                file.write(tutor.to_string() + '\n')

    def register_user(self, username: str, password: str, email: str) -> None:
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.save_users()

    def request_tutoring(self, subject: str, details: str, preferred_date: str) -> None:
        new_request = TutoringRequest(subject, details, preferred_date)
        self.tutoring_requests.append(new_request)
        self.save_tutoring_requests()

    def contact_support(self, message: str) -> None:
        # Placeholder for contacting support functionality
        print(f"Support message: {message}")

network = PeerTutoringNetwork()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in network.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        network.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/view_tutors')
def view_tutors():
    return render_template('view_tutors.html', tutors=network.tutors)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        message = request.form['message']
        network.contact_support(message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        network.request_tutoring(subject, details, preferred_date)
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8547, debug=False)
