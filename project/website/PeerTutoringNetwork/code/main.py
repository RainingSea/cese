from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users():
        users = {}
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        except FileNotFoundError:
            open('users.txt', 'w').close()  # Create file if it doesn't exist
        return users

class Tutor:
    def __init__(self, name: str, subject: str):
        self.name = name
        self.subject = subject

    def save(self):
        with open('tutors.txt', 'a') as f:
            f.write(f"{self.name}|{self.subject}\n")

    @staticmethod
    def load_tutors():
        tutors = []
        try:
            with open('tutors.txt', 'r') as f:
                for line in f:
                    name, subject = line.strip().split('|')
                    tutors.append(Tutor(name, subject))
        except FileNotFoundError:
            open('tutors.txt', 'w').close()  # Create file if it doesn't exist
        return tutors

class TutoringRequest:
    def __init__(self, username: str, subject: str, details: str, preferred_date: str):
        self.username = username
        self.subject = subject
        self.details = details
        self.preferred_date = preferred_date

    def save(self):
        with open('requests.txt', 'a') as f:
            f.write(f"{self.username}|{self.subject}|{self.details}|{self.preferred_date}\n")

    @staticmethod
    def load_requests():
        requests = []
        try:
            with open('requests.txt', 'r') as f:
                for line in f:
                    username, subject, details, preferred_date = line.strip().split('|')
                    requests.append(TutoringRequest(username, subject, details, preferred_date))
        except FileNotFoundError:
            open('requests.txt', 'w').close()  # Create file if it doesn't exist
        return requests

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_users()
    
    if username in users and users[username][0] == password:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tutors = Tutor.load_tutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/request_tutoring', methods=['POST'])
def request_tutoring():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    subject = request.form['subject']
    details = request.form['details']
    preferred_date = request.form['preferred_date']
    tutoring_request = TutoringRequest(session['username'], subject, details, preferred_date)
    tutoring_request.save()
    
    return redirect(url_for('dashboard'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = User.load_users()
    email = users[session['username']][1]
    return render_template('profile.html', username=session['username'], email=email)

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
        with open('contact_requests.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8166, debug=True)
