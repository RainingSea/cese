from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users[username] = {'password': password, 'email': email}
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username]['password'] == password:
            session['username'] = username
            return True
        return False

    def get_user_profile(self, username: str) -> dict:
        return self.users.get(username, {})

class TutoringRequestManager:
    def __init__(self, requests_file):
        self.requests_file = requests_file
        self.load_requests()

    def load_requests(self):
        self.requests = {}
        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r') as file:
                for line in file:
                    username, subject, details, date = line.strip().split('|')
                    if username not in self.requests:
                        self.requests[username] = []
                    self.requests[username].append({'subject': subject, 'details': details, 'date': date})

    def request_tutoring(self, username: str, subject: str, details: str, date: str) -> bool:
        with open(self.requests_file, 'a') as file:
            file.write(f"{username}|{subject}|{details}|{date}\n")
        if username not in self.requests:
            self.requests[username] = []
        self.requests[username].append({'subject': subject, 'details': details, 'date': date})
        return True

    def cancel_request(self, username: str, request_id: int) -> bool:
        if username in self.requests and 0 <= request_id < len(self.requests[username]):
            del self.requests[username][request_id]
            self.save_requests()
            return True
        return False

    def save_requests(self):
        with open(self.requests_file, 'w') as file:
            for username, requests in self.requests.items():
                for req in requests:
                    file.write(f"{username}|{req['subject']}|{req['details']}|{req['date']}\n")

    def get_requests(self, username: str) -> list:
        return self.requests.get(username, [])

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if user_manager.register(username, password, email):
        flash('Registration successful!')
        return redirect('/')
    else:
        flash('Username already exists.')
        return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/dashboard')
    else:
        flash('Invalid credentials.')
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to access the dashboard.')
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/request_tutoring')
def request_tutoring():
    if 'username' not in session:
        flash('Please log in to request tutoring.')
        return redirect('/')
    return render_template('request_tutoring.html')

@app.route('/submit_request', methods=['POST'])
def submit_request():
    username = session.get('username')
    subject = request.form['subject']
    details = request.form['details']
    date = request.form['date']
    tutoring_request_manager.request_tutoring(username, subject, details, date)
    flash('Tutoring request submitted successfully!')
    return redirect('/dashboard')

@app.route('/view_requests')
def view_requests():
    username = session.get('username')
    if not username:
        flash('Please log in to view your requests.')
        return redirect('/')
    requests = tutoring_request_manager.get_requests(username)
    return render_template('view_requests.html', requests=requests)

@app.route('/cancel_request/<int:request_id>', methods=['POST'])
def cancel_request(request_id):
    username = session.get('username')
    if tutoring_request_manager.cancel_request(username, request_id):
        flash('Tutoring request canceled successfully!')
    else:
        flash('Failed to cancel tutoring request.')
    return redirect('/view_requests')

@app.route('/contact_support')
def contact_support():
    if 'username' not in session:
        flash('Please log in to contact support.')
        return redirect('/')
    return render_template('contact_support.html')

@app.route('/view_available_tutors')
def view_available_tutors():
    if 'username' not in session:
        flash('Please log in to view available tutors.')
        return redirect('/')
    return render_template('view_tutors.html', tutors=tutors_manager.get_available_tutors())

class TutorsManager:
    def __init__(self, tutors_file):
        self.tutors_file = tutors_file
        self.load_tutors()

    def load_tutors(self):
        self.tutors = []
        if os.path.exists(self.tutors_file):
            with open(self.tutors_file, 'r') as file:
                for line in file:
                    name, subject, availability = line.strip().split('|')
                    self.tutors.append({'name': name, 'subject': subject, 'availability': availability})

    def get_available_tutors(self):
        return self.tutors

if __name__ == '__main__':
    user_manager = UserManager('users.txt')
    tutoring_request_manager = TutoringRequestManager('tutoring_requests.txt')
    tutors_manager = TutorsManager('tutors.txt')
    app.run(port=8393, debug=False)
