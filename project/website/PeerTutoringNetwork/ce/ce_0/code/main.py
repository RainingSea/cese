from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILES = {
    'users': 'users.txt',
    'requests': 'requests.txt',
    'contacts': 'contacts.txt'
}

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open(DATA_FILES['users'], 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str, username: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date
        self.username = username

    def save(self):
        with open(DATA_FILES['requests'], 'a') as f:
            f.write(f"{self.subject}|{self.details}|{self.preferred_date}|{self.username}\n")

class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open(DATA_FILES['contacts'], 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")

class PeerTutoringNetwork:
    def register_user(self, username: str, password: str, email: str) -> bool:
        user = User(username, password, email)
        user.save()
        return True

    def login_user(self, username: str, password: str) -> bool:
        with open(DATA_FILES['users'], 'r') as f:
            for line in f:
                stored_username, stored_password, _ = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def view_tutors(self) -> List[str]:
        # Placeholder for tutor data
        return ["Tutor1", "Tutor2", "Tutor3"]

    def request_tutoring(self, subject: str, details: str, preferred_date: str, username: str) -> None:
        request = TutoringRequest(subject, details, preferred_date, username)
        request.save()

    def contact_support(self, name: str, email: str, message: str) -> None:
        contact = Contact(name, email, message)
        contact.save()

    def cancel_request(self, username: str) -> None:
        # Placeholder for request cancellation logic
        pass

network = PeerTutoringNetwork()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if network.login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
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
    tutors = network.view_tutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        network.contact_support(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8718, debug=False)
