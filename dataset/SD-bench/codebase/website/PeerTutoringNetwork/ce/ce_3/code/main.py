from flask import Flask, render_template, request, redirect, url_for
from user import User
from tutoring_request import TutoringRequest
from tutor import Tutor

app = Flask(__name__)

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users[username] = User(username, password, email)
    return users

def load_tutors():
    tutors = []
    with open('tutors.txt', 'r') as file:
        for line in file:
            username, subject = line.strip().split('|')
            tutors.append(Tutor(username, subject))
    return tutors

def load_tutoring_requests():
    requests = []
    with open('tutoring_requests.txt', 'r') as file:
        for line in file:
            subject, details, preferred_date, username = line.strip().split('|')
            requests.append(TutoringRequest(subject, details, preferred_date, username))
    return requests

users = load_users()
tutors = load_tutors()
tutoring_requests = load_tutoring_requests()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        users[username] = new_user
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle contact support logic here
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        username = request.form['username']  # Assume username is passed from session
        new_request = TutoringRequest(subject, details, preferred_date, username)
        tutoring_requests.append(new_request)
        with open('tutoring_requests.txt', 'a') as file:
            file.write(f"{subject}|{details}|{preferred_date}|{username}\n")
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

if __name__ == '__main__':
    app.run(port=8678, debug=False)
