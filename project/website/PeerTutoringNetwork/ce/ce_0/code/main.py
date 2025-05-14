from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register_user(self, username, password, email):
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username}|{password}|{email}\n")
            return True
        except IOError:
            return False

    def authenticate(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username and parts[1] == password:
                        return True
            return False
        except FileNotFoundError:
            return False

    def get_user(self, username):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username:
                        return {'username': parts[0], 'email': parts[2]}
            return None
        except FileNotFoundError:
            return None

class TutorManager:
    def __init__(self, tutors_file='tutors.txt'):
        self.tutors_file = tutors_file

    def get_all_tutors(self):
        tutors = []
        try:
            with open(self.tutors_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    tutors.append({
                        'username': parts[0],
                        'subjects': parts[1].split(','),
                        'availability': parts[2]
                    })
        except FileNotFoundError:
            pass
        return tutors

    def add_tutor(self, username, subjects, availability):
        try:
            with open(self.tutors_file, 'a') as f:
                f.write(f"{username}|{','.join(subjects)}|{availability}\n")
            return True
        except IOError:
            return False

class RequestManager:
    def __init__(self, requests_file='requests.txt'):
        self.requests_file = requests_file

    def create_request(self, requester, tutor, subject, details, date):
        try:
            with open(self.requests_file, 'a') as f:
                f.write(f"{requester}|{tutor}|{subject}|{details}|{date}|pending\n")
            return True
        except IOError:
            return False

    def cancel_request(self, request_id):
        try:
            with open(self.requests_file, 'r') as f:
                requests = f.readlines()
            
            if 0 <= request_id < len(requests):
                requests.pop(request_id)
                
                with open(self.requests_file, 'w') as f:
                    f.writelines(requests)
                return True
            return False
        except IOError:
            return False

    def get_user_requests(self, username):
        user_requests = []
        try:
            with open(self.requests_file, 'r') as f:
                for idx, line in enumerate(f):
                    parts = line.strip().split('|')
                    if parts[0] == username or parts[1] == username:
                        user_requests.append({
                            'id': idx,
                            'requester': parts[0],
                            'tutor': parts[1],
                            'subject': parts[2],
                            'details': parts[3],
                            'date': parts[4],
                            'status': parts[5]
                        })
        except FileNotFoundError:
            pass
        return user_requests

user_manager = UserManager()
tutor_manager = TutorManager()
request_manager = RequestManager()

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
        if user_manager.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register_user(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
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
    all_tutors = tutor_manager.get_all_tutors()
    return render_template('tutors.html', tutors=all_tutors)

@app.route('/request', methods=['GET', 'POST'])
def request_tutor():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tutor = request.form['tutor']
        subject = request.form['subject']
        details = request.form['details']
        date = request.form['date']
        if request_manager.create_request(session['username'], tutor, subject, details, date):
            return redirect(url_for('dashboard'))
        return render_template('request.html', error='Request failed')
    
    tutors = tutor_manager.get_all_tutors()
    return render_template('request.html', tutors=tutors)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = user_manager.get_user(session['username'])
    requests = request_manager.get_user_requests(session['username'])
    return render_template('profile.html', user=user, requests=requests)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        try:
            with open('contacts.txt', 'a') as f:
                f.write(f"{name}|{email}|{message}|{timestamp}\n")
            return render_template('contact.html', success=True)
        except IOError:
            return render_template('contact.html', error='Failed to send message')
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8028, debug=False)
