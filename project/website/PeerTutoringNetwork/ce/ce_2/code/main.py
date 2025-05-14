from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
USERS_FILE = 'users.txt'
TUTORS_FILE = 'tutors.txt'
REQUESTS_FILE = 'requests.txt'
CONTACTS_FILE = 'contacts.txt'

def load_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append({'username': username, 'password': password, 'email': email})
    return users

def save_user(username, password, email):
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}|{password}|{email}\n")

def load_tutors():
    tutors = []
    if os.path.exists(TUTORS_FILE):
        with open(TUTORS_FILE, 'r') as f:
            for line in f:
                name, subjects, availability = line.strip().split('|')
                tutors.append({'name': name, 'subjects': subjects.split(','), 'availability': availability})
    return tutors

def save_request(username, subject, details, date):
    with open(REQUESTS_FILE, 'a') as f:
        f.write(f"{username}|{subject}|{details}|{date}\n")

def load_requests(username=None):
    requests = []
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'r') as f:
            for line in f:
                req_username, subject, details, date = line.strip().split('|')
                if username is None or req_username == username:
                    requests.append({'username': req_username, 'subject': subject, 'details': details, 'date': date})
    return requests

def save_contact(name, email, message):
    with open(CONTACTS_FILE, 'a') as f:
        f.write(f"{name}|{email}|{message}\n")

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                session['email'] = user['email']
                return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        users = load_users()
        if any(user['username'] == username for user in users):
            return render_template('register.html', error='Username already exists')
        save_user(username, password, email)
        session['username'] = username
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tutors')
def tutors():
    if 'username' not in session:
        return redirect(url_for('login'))
    tutors_list = load_tutors()
    return render_template('tutors.html', tutors=tutors_list)

@app.route('/request', methods=['GET', 'POST'])
def request_tutor():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        date = request.form['date']
        save_request(session['username'], subject, details, date)
        return redirect(url_for('dashboard'))
    return render_template('request.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html', username=session['username'], email=session['email'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        save_contact(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8030, debug=False)
