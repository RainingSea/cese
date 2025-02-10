from flask import Flask, render_template, request, redirect, session
from typing import List
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
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

    def save(self) -> None:
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}\n")

class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self) -> None:
        with open('requests.txt', 'a') as f:
            f.write(f"{self.username}|{self.subject}|{self.details}|{self.preferred_date}\n")

class App:
    def __init__(self):
        self.users = []
        self.tutors = []
        self.requests = []
        self.load_data()

    def load_data(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    user_data = line.strip().split('|')
                    self.users.append(User(user_data[0], user_data[1], user_data[2]))
        if os.path.exists('tutors.txt'):
            with open('tutors.txt', 'r') as f:
                for line in f:
                    tutor_data = line.strip().split('|')
                    self.tutors.append(Tutor(tutor_data[0], tutor_data[1]))
        if os.path.exists('requests.txt'):
            with open('requests.txt', 'r') as f:
                for line in f:
                    request_data = line.strip().split('|')
                    self.requests.append(TutoringRequest(request_data[0], request_data[1], request_data[2], request_data[3]))

    def register(self, username: str, password: str, email: str) -> None:
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)

    def login(self, username: str, password: str) -> bool:
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return True
        return False

    def view_tutors(self) -> List[Tutor]:
        return self.tutors

    def request_tutoring(self, username: str, subject: str, details: str, preferred_date: str) -> None:
        new_request = TutoringRequest(username, subject, details, preferred_date)
        new_request.save()
        self.requests.append(new_request)

    def contact_support(self, name: str, email: str, message: str) -> None:
        # Here you would handle sending a message to support
        pass

app_instance = App()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        app_instance.register(username, password, email)
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    tutors = app_instance.view_tutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile_page():
    username = session.get('username')
    user = User.load(username)
    return render_template('profile.html', user=user)

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        app_instance.contact_support(name, email, message)
        return redirect('/dashboard')
    return render_template('contact.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring_page():
    if request.method == 'POST':
        username = session.get('username')
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        app_instance.request_tutoring(username, subject, details, preferred_date)
        return redirect('/dashboard')
    return render_template('request_tutoring.html')

if __name__ == '__main__':
    app.run(port=8722, debug=False)
