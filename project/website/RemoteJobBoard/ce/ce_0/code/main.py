from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.applied_jobs = []

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def login(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username and user_data[1] == self.password:
                    return True
        return False

    def edit_profile(self, new_username=None, new_password=None):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    if new_username:
                        user_data[0] = new_username
                    if new_password:
                        user_data[1] = new_password
                users.append('|'.join(user_data))
        
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user}\n")

class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

    def post_job(self):
        with open('jobs.txt', 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    def apply(self, username):
        with open('users.txt', 'r') as f:
            users = f.readlines()
        
        for i, line in enumerate(users):
            if line.startswith(username):
                users[i] = line.strip() + f"|{self.title}\n"
        
        with open('users.txt', 'w') as f:
            f.writelines(users)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.register()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/job_listing')
def job_listing():
    jobs = []
    with open('jobs.txt', 'r') as f:
        for line in f:
            job_data = line.strip().split('|')
            jobs.append(Job(job_data[0], job_data[1], job_data[2]))
    return render_template('job_listing.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.post_job()
        return redirect(url_for('job_listing'))
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    return render_template('profile.html', username=username)

if __name__ == '__main__':
    app.run(port=8234, debug=False)
