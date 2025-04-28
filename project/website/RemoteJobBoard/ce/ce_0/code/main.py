from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False  # User already exists
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def get_user_profile(self, username: str) -> dict:
        for user in self.users:
            if user[0] == username:
                return {'username': user[0]}
        return {}

class JobManager:
    def __init__(self):
        self.jobs = self.load_jobs()

    def load_jobs(self):
        if not os.path.exists('jobs.txt'):
            return []
        with open('jobs.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def post_job(self, title: str, company: str, description: str) -> bool:
        job_id = len(self.jobs) + 1
        self.jobs.append([job_id, title, company, description])
        with open('jobs.txt', 'a') as file:
            file.write(f"{job_id}|{title}|{company}|{description}\n")
        return True

    def browse_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        with open('applied_jobs.txt', 'a') as file:
            file.write(f"{username}|{job_id}\n")
        return True

user_manager = UserManager()
job_manager = JobManager()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=job_manager.browse_jobs())

@app.route('/browse_jobs')
def browse_jobs():
    return render_template('browse_jobs.html', jobs=job_manager.browse_jobs())

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    user_profile = user_manager.get_user_profile(session.get('username'))
    return render_template('profile.html', profile=user_profile)

if __name__ == '__main__':
    app.run(port=8406, debug=False)
