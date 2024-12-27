from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def add_user(self, user: User) -> None:
        self.users.append(user)
        self.save_users()

    def get_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def load_users(self) -> list:
        users = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> None:
        with open(self.filename, 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")

class Tutor:
    def __init__(self, name: str, subject: str, availability: str):
        self.name = name
        self.subject = subject
        self.availability = availability

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'subject': self.subject,
            'availability': self.availability
        }

class TutorManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tutors = self.load_tutors()

    def load_tutors(self) -> list:
        tutors = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    name, subject, availability = line.strip().split('|')
                    tutors.append(Tutor(name, subject, availability))
        except FileNotFoundError:
            pass
        return tutors

class TutoringRequest:
    def __init__(self, subject: str, details: str, preferred_date: str):
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def to_dict(self) -> dict:
        return {
            'subject': self.subject,
            'details': self.details,
            'preferred_date': self.preferred_date
        }

class RequestManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.requests = self.load_requests()

    def add_request(self, request: TutoringRequest) -> None:
        self.requests.append(request)
        self.save_requests()

    def load_requests(self) -> list:
        requests = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    subject, details, preferred_date = line.strip().split('|')
                    requests.append(TutoringRequest(subject, details, preferred_date))
        except FileNotFoundError:
            pass
        return requests

    def save_requests(self) -> None:
        with open(self.filename, 'w') as file:
            for request in self.requests:
                file.write(f"{request.subject}|{request.details}|{request.preferred_date}\n")

tutor_manager = TutorManager('tutors.txt')
user_manager = UserManager('users.txt')
request_manager = RequestManager('requests.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_manager.get_user(username)
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        user_manager.add_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tutors = tutor_manager.tutors
    
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        new_request = TutoringRequest(subject, details, preferred_date)
        request_manager.add_request(new_request)
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', username=session['username'], tutors=tutors, requests=request_manager.requests)

@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = user_manager.get_user(session['username'])
    return render_template('profile.html', username=user.username, email=user.email)

@app.route('/cancel_request/<int:request_id>', methods=['POST'])
def cancel_request(request_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    if 0 <= request_id < len(request_manager.requests):
        del request_manager.requests[request_id]
        request_manager.save_requests()
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_requests.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)