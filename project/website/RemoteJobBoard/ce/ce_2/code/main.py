from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append({'username': username, 'password': password})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def get_user_profile(self, username: str) -> dict:
        for user in self.users:
            if user['username'] == username:
                return user
        return {}

class JobManager:
    def __init__(self):
        self.jobs = self.load_jobs()

    def load_jobs(self):
        jobs = []
        with open('jobs.txt', 'r') as file:
            for line in file:
                title, company, description = line.strip().split('|')
                jobs.append({'title': title, 'company': company, 'description': description})
        return jobs

    def post_job(self, title: str, company: str, description: str) -> bool:
        self.jobs.append({'title': title, 'company': company, 'description': description})
        with open('jobs.txt', 'a') as file:
            file.write(f"{title}|{company}|{description}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, job_id: int, username: str) -> bool:
        # Placeholder for job application logic
        return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = job_manager.get_all_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    user_profile = user_manager.get_user_profile(session['username'])
    return render_template('profile.html', profile=user_profile)

if __name__ == '__main__':
    user_manager = UserManager()
    job_manager = JobManager()
    app.run(port=8236, debug=False)
