from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def save(self):
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}\n")

class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('requests.txt', 'a') as f:
            f.write(f"{self.username}|{self.subject}|{self.details}|{self.preferred_date}\n")

class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contacts.txt', 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")

def load_users() -> List[User]:
    users = []
    try:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass
    return users

def load_tutors() -> List[Tutor]:
    tutors = []
    try:
        with open('tutors.txt', 'r') as f:
            for line in f:
                name, subject = line.strip().split('|')
                tutors.append(Tutor(name, subject))
    except FileNotFoundError:
        pass
    return tutors

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
        return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        tutoring_request = TutoringRequest(session['username'], subject, details, preferred_date)
        tutoring_request.save()
        return redirect(url_for('dashboard'))

    tutors = load_tutors()
    return render_template('dashboard.html', username=session['username'], tutors=tutors)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_request = Contact(name, email, message)
        contact_request.save()
        return redirect(url_for('login'))  # Redirect to login or a thank you page

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8164, debug=True)
