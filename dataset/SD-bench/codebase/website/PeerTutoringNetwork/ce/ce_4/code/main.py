from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tutor import Tutor
from tutoring_request import TutoringRequest
from contact import Contact
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    return users

def load_tutors():
    tutors = []
    if os.path.exists('tutors.txt'):
        with open('tutors.txt', 'r') as f:
            for line in f:
                name, subject = line.strip().split('|')
                tutors.append(Tutor(name, subject))
    return tutors

def load_requests():
    requests = []
    if os.path.exists('requests.txt'):
        with open('requests.txt', 'r') as f:
            for line in f:
                username, subject, details, preferred_date = line.strip().split('|')
                requests.append(TutoringRequest(username, subject, details, preferred_date))
    return requests

def load_contacts():
    contacts = []
    if os.path.exists('contacts.txt'):
        with open('contacts.txt', 'r') as f:
            for line in f:
                name, email, message = line.strip().split('|')
                contacts.append(Contact(name, email, message))
    return contacts

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

@app.route('/view_tutors')
def view_tutors():
    tutors = load_tutors()
    return render_template('view_tutors.html', tutors=tutors)

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        username = session['username']
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        request = TutoringRequest(username, subject, details, preferred_date)
        request.save()
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = Contact(name, email, message)
        contact.save()
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8679, debug=False)
