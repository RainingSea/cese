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

    @staticmethod
    def load(username: str) -> 'User':
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def save(self):
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}\n")

    @staticmethod
    def load_all() -> List['Tutor']:
        tutors = []
        with open('tutors.txt', 'r') as f:
            for line in f:
                tutor_data = line.strip().split('|')
                tutors.append(Tutor(tutor_data[0], tutor_data[1]))
        return tutors

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('requests.txt', 'a') as f:
            f.write(f"{self.subject}|{self.details}|{self.preferred_date}\n")

    @staticmethod
    def load_all() -> List['TutoringRequest']:
        requests = []
        with open('requests.txt', 'r') as f:
            for line in f:
                request_data = line.strip().split('|')
                requests.append(TutoringRequest(request_data[0], request_data[1], request_data[2]))
        return requests

    @staticmethod
    def cancel(subject: str, preferred_date: str) -> bool:
        requests = TutoringRequest.load_all()
        with open('requests.txt', 'w') as f:
            for request in requests:
                if request.subject != subject or request.preferred_date != preferred_date:
                    f.write(f"{request.subject}|{request.details}|{request.preferred_date}\n")
                else:
                    return True  # Successfully canceled
        return False  # No matching request found

class SupportMessage:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('support_messages.txt', 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    user = User.load(username)
    if user and user.password == password:
        session['username'] = user.username
        session['email'] = user.email
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/view_tutors')
def view_tutors():
    if 'username' not in session:
        return redirect(url_for('login'))
    tutors = Tutor.load_all()
    return render_template('view_tutors.html', tutors=tutors)

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        tutoring_request = TutoringRequest(subject, details, preferred_date)
        tutoring_request.save()
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

@app.route('/cancel_request', methods=['POST'])
def cancel_request():
    if 'username' not in session:
        return redirect(url_for('login'))
    subject = request.form['subject']
    preferred_date = request.form['preferred_date']
    if TutoringRequest.cancel(subject, preferred_date):
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        support_message = SupportMessage(name, email, message)
        support_message.save()
        return redirect(url_for('dashboard'))
    return render_template('contact_us.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8063, debug=False)
