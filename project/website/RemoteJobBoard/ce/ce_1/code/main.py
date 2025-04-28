from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            users = {}
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
            return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def get_user_profile(self, username: str) -> dict:
        return {"username": username}

class JobManager:
    def __init__(self):
        self.jobs = self.load_jobs()

    def load_jobs(self):
        if not os.path.exists('jobs.txt'):
            return []
        with open('jobs.txt', 'r') as file:
            jobs = []
            for line in file:
                title, company, description = line.strip().split('|')
                jobs.append({"title": title, "company": company, "description": description})
            return jobs

    def post_job(self, title: str, company: str, description: str) -> bool:
        self.jobs.append({"title": title, "company": company, "description": description})
        with open('jobs.txt', 'a') as file:
            file.write(f"{title}|{company}|{description}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        if job_id < 0 or job_id >= len(self.jobs):
            return False
        with open('applied_jobs.txt', 'a') as file:
            file.write(f"{username}|{job_id}\n")
        return True

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.job_manager = JobManager()

    def main(self):
        app.run(port=8407, debug=False)

main_app = Main()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if main_app.user_manager.register(username, password):
        return redirect(url_for('login'))
    return "Registration failed", 400

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/browse_jobs')
def browse_jobs():
    jobs = main_app.job_manager.get_all_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/post_job', methods=['POST'])
def post_job():
    title = request.form['title']
    company = request.form['company']
    description = request.form['description']
    main_app.job_manager.post_job(title, company, description)
    return redirect(url_for('browse_jobs'))

if __name__ == '__main__':
    main_app.main()