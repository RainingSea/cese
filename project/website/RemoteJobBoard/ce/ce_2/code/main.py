from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_FILES = {
    'users': 'users.txt',
    'jobs': 'jobs.txt',
    'applied_jobs': 'applied_jobs.txt'
}

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open(DATA_FILES['users'], 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str):
        with open(DATA_FILES['users'], 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open(DATA_FILES['jobs'], 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_all():
        jobs = []
        with open(DATA_FILES['jobs'], 'r') as f:
            for line in f:
                job_data = line.strip().split('|')
                jobs.append(Job(job_data[0], job_data[1], job_data[2]))
        return jobs

class Application:
    def __init__(self, username: str, job_title: str):
        self.username = username
        self.job_title = job_title

    def save(self):
        with open(DATA_FILES['applied_jobs'], 'a') as f:
            f.write(f"{self.username}|{self.job_title}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = Job.load_all()
    return render_template('home.html', jobs=jobs)

@app.route('/browse_jobs')
def browse_jobs():
    jobs = Job.load_all()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.save()
        return redirect(url_for('home'))
    return render_template('post_job.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port=8192, debug=False)
