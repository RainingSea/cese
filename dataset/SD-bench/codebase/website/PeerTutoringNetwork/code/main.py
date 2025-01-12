from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class Tutor:
    def __init__(self, name: str, subject: str, availability: str):
        self.name = name
        self.subject = subject
        self.availability = availability

    def save(self):
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}|{self.availability}\n")

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('requests.txt', 'a') as f:
            f.write(f"{self.subject}|{self.details}|{self.preferred_date}\n")

class Application:
    def register_user(self, username: str, password: str, email: str):
        user = User(username, password, email)
        user.save()

    def login_user(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                u, p, _ = line.strip().split('|')
                if u == username and p == password:
                    session['username'] = username
                    return True
        return False

    def view_tutors(self) -> list:
        tutors = []
        with open('tutors.txt', 'r') as f:
            for line in f:
                name, subject, availability = line.strip().split('|')
                tutors.append(Tutor(name, subject, availability))
        return tutors

    def request_tutoring(self, subject: str, details: str, preferred_date: str):
        request = TutoringRequest(subject, details, preferred_date)
        request.save()

    def cancel_request(self, request_id: int):
        with open('requests.txt', 'r') as f:
            requests = f.readlines()
        if 0 <= request_id < len(requests):
            requests.pop(request_id)
        with open('requests.txt', 'w') as f:
            f.writelines(requests)

    def contact_support(self, name: str, email: str, message: str):
        with open('support_requests.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app_instance.login_user(username, password):
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        app_instance.register_user(username, password, email)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    tutors = app_instance.view_tutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile():
    return render_template('profile.html', username=session.get('username'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        app_instance.contact_support(name, email, message)
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app_instance = Application()
    app.run(port=8317, debug=False)
