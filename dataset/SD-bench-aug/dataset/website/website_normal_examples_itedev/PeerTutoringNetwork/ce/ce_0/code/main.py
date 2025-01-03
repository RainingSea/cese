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
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

def load_users() -> List[User]:
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass
    return users

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def save(self):
        with open('tutors.txt', 'a') as file:
            file.write(f"{self.name}|{self.subject}\n")

def load_tutors() -> List[Tutor]:
    tutors = []
    try:
        with open('tutors.txt', 'r') as file:
            for line in file:
                name, subject = line.strip().split('|')
                tutors.append(Tutor(name, subject))
    except FileNotFoundError:
        pass
    return tutors

class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('requests.txt', 'a') as file:
            file.write(f"{self.username}|{self.subject}|{self.details}|{self.preferred_date}\n")

class Contact:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contacts.txt', 'a') as file:
            file.write(f"{self.name}|{self.email}|{self.message}\n")

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
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/view_tutors')
def view_tutors():
    if 'username' in session:
        tutors = load_tutors()
        return render_template('view_tutors.html', tutors=tutors)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        users = load_users()
        user_info = next((user for user in users if user.username == username), None)
        return render_template('profile.html', username=user_info.username, email=user_info.email)
    return redirect(url_for('login'))

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            subject = request.form['subject']
            details = request.form['details']
            preferred_date = request.form['preferred_date']
            tutoring_request = TutoringRequest(username, subject, details, preferred_date)
            tutoring_request.save()
            return redirect(url_for('dashboard'))
        return render_template('request_tutoring.html')
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact_support():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = Contact(name, email, message)
        contact.save()
        return redirect(url_for('dashboard'))
    return render_template('contact_us.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)