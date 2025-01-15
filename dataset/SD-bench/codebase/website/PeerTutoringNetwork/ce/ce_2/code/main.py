from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tutoring_request import TutoringRequest
from support_message import SupportMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users.append(User(username, password, email))
    return users

def load_tutoring_requests():
    requests = []
    with open('tutoring_requests.txt', 'r') as file:
        for line in file:
            subject, details, preferred_date = line.strip().split('|')
            requests.append(TutoringRequest(subject, details, preferred_date))
    return requests

def load_support_messages():
    messages = []
    with open('support_messages.txt', 'r') as file:
        for line in file:
            name, email, message = line.strip().split('|')
            messages.append(SupportMessage(name, email, message))
    return messages

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        support_message = SupportMessage(name, email, message)
        support_message.save()
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        tutoring_request = TutoringRequest(subject, details, preferred_date)
        tutoring_request.save()
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

if __name__ == '__main__':
    app.run(port=8677, debug=False)
