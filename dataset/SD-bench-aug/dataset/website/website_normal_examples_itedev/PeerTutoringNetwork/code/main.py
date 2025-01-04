from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from tutor import Tutor
from tutoring_request import TutoringRequest
from contact import Contact

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the text file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except ValueError:
        print("Error loading users: Check the format of users.txt")
    return users

# Save users to the text file
def save_user(user):
    with open('users.txt', 'a') as file:
        file.write(f"{user.username}|{user.password}|{user.email}\n")

# Load tutors from the text file
def load_tutors():
    tutors = []
    try:
        with open('tutors.txt', 'r') as file:
            for line in file:
                name, subject = line.strip().split('|')
                tutors.append(Tutor(name, subject))
    except ValueError:
        print("Error loading tutors: Check the format of tutors.txt")
    return tutors

# Load tutoring requests from the text file
def load_requests():
    requests = []
    try:
        with open('requests.txt', 'r') as file:
            for line in file:
                username, subject, details, preferred_date = line.strip().split('|')
                requests.append(TutoringRequest(username, subject, details, preferred_date))
    except ValueError:
        print("Error loading requests: Check the format of requests.txt")
    return requests

# Save tutoring request to the text file
def save_request(request):
    with open('requests.txt', 'a') as file:
        file.write(f"{request.username}|{request.subject}|{request.details}|{request.preferred_date}\n")

# Load contact messages from the text file
def load_contacts():
    contacts = []
    try:
        with open('contacts.txt', 'r') as file:
            for line in file:
                name, email, message = line.strip().split('|')
                contacts.append(Contact(name, email, message))
    except ValueError:
        print("Error loading contacts: Check the format of contacts.txt")
    return contacts

# Save contact message to the text file
def save_contact(contact):
    with open('contacts.txt', 'a') as file:
        file.write(f"{contact.name}|{contact.email}|{contact.message}\n")

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
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

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        save_user(new_user)
        return redirect(url_for('login'))
    return render_template('registration.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    tutors = load_tutors()
    return render_template('dashboard.html', username=session['username'], tutors=tutors)

# View Tutors route
@app.route('/view_tutors')
def view_tutors():
    if 'username' not in session:
        return redirect(url_for('login'))
    tutors = load_tutors()
    return render_template('view_tutors.html', tutors=tutors)

# Request Tutoring route
@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        new_request = TutoringRequest(session['username'], subject, details, preferred_date)
        save_request(new_request)
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

# Profile route
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    users = load_users()
    user_info = next((user for user in users if user.username == username), None)
    return render_template('profile.html', user=user_info)

# Contact Support route
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_support():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_contact = Contact(name, email, message)
        save_contact(new_contact)
        return redirect(url_for('dashboard'))
    return render_template('contact_us.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)