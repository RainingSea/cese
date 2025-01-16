from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def apply_job(self, job_id: str):
        self.applied_jobs.append(job_id)

    def edit_profile(self, new_email: str):
        self.email = new_email

class Job:
    def __init__(self, job_id: str, title: str, company: str, description: str):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.description = description

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except FileNotFoundError:
        pass
    return users

def load_jobs():
    jobs = []
    try:
        with open('jobs.txt', 'r') as file:
            for line in file:
                job_id, title, company, description = line.strip().split('|')
                jobs.append(Job(job_id, title, company, description))
    except FileNotFoundError:
        pass
    return jobs

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/browse_jobs')
def browse_jobs():
    jobs = load_jobs()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_id = request.form['job_id']
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        with open('jobs.txt', 'a') as file:
            file.write(f"{job_id}|{title}|{company}|{description}\n")
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile')
def view_profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    new_email = request.form['email']
    # Placeholder for user editing logic
    return redirect(url_for('view_profile'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8487, debug=False)
