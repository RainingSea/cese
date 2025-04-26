from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def register(self):
        if self.username and self.password and self.email:
            with open('users.txt', 'a') as f:
                f.write(f"{self.username}|{self.password}|{self.email}\n")
            return True
        return False

    def login(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username and user_data[1] == self.password:
                    return True
        return False

    def edit_profile(self, new_email):
        self.email = new_email
        # Update the users.txt file
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    user_data[2] = self.email
                users.append('|'.join(user_data))
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user}\n")
        return True

class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

    def post_job(self):
        if self.title and self.company and self.description:
            with open('jobs.txt', 'a') as f:
                f.write(f"{self.title}|{self.company}|{self.description}\n")
            return True
        return False

    def apply_job(self, user):
        with open('applied_jobs.txt', 'a') as f:
            f.write(f"{user.username}|{self.title}\n")
        return True

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
        if user.register():
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/job_listings')
def job_listings():
    jobs = []
    with open('jobs.txt', 'r') as f:
        for line in f:
            job_data = line.strip().split('|')
            jobs.append(Job(job_data[0], job_data[1], job_data[2]))
    return render_template('job_listings.html', jobs=jobs)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        if job.post_job():
            return redirect(url_for('job_listings'))
    return render_template('job_posting.html')

if __name__ == '__main__':
    app.run(port=8235, debug=False)
