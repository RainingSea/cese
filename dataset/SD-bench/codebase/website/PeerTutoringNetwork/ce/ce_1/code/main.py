from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def to_string(self) -> str:
        return f"{self.name}|{self.subject}"

class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def to_string(self) -> str:
        return f"{self.username}|{self.subject}|{self.details}|{self.preferred_date}"

class Application:
    def __init__(self):
        self.users: List[User] = []
        self.tutors: List[Tutor] = []
        self.requests: List[TutoringRequest] = []
        self.load_users()
        self.load_tutors()
        self.load_requests()

    def load_users(self) -> None:
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                self.users.append(User(username, password, email))

    def save_users(self) -> None:
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(user.to_string() + '\n')

    def load_tutors(self) -> None:
        with open('tutors.txt', 'r') as f:
            for line in f:
                name, subject = line.strip().split('|')
                self.tutors.append(Tutor(name, subject))

    def save_tutors(self) -> None:
        with open('tutors.txt', 'w') as f:
            for tutor in self.tutors:
                f.write(tutor.to_string() + '\n')

    def load_requests(self) -> None:
        with open('tutoring_requests.txt', 'r') as f:
            for line in f:
                username, subject, details, preferred_date = line.strip().split('|')
                self.requests.append(TutoringRequest(username, subject, details, preferred_date))

    def save_requests(self) -> None:
        with open('tutoring_requests.txt', 'w') as f:
            for request in self.requests:
                f.write(request.to_string() + '\n')

    def register_user(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.save_users()
        return True

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                session['username'] = username
                return True
        return False

    def request_tutoring(self, username: str, subject: str, details: str, preferred_date: str) -> bool:
        new_request = TutoringRequest(username, subject, details, preferred_date)
        self.requests.append(new_request)
        self.save_requests()
        return True

    def cancel_request(self, username: str, subject: str) -> bool:
        for request in self.requests:
            if request.username == username and request.subject == subject:
                self.requests.remove(request)
                self.save_requests()
                return True
        return False

app_instance = Application()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if app_instance.register_user(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', tutors=app_instance.tutors)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = next((u for u in app_instance.users if u.username == username), None)
    return render_template('profile.html', user=user)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8676, debug=False)
