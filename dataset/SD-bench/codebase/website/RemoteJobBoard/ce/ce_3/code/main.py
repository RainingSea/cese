from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from auth import Auth
from profile import Profile
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and jobs from files
def load_users():
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]
    return []

def load_jobs():
    if os.path.exists('jobs.txt'):
        with open('jobs.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]
    return []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth = Auth()
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    jobs = load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/browse_jobs')
def browse_jobs():
    jobs = load_jobs()
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
    user = Profile(session.get('username'))
    user_info = user.view_profile()
    return render_template('profile.html', user=user_info)

if __name__ == '__main__':
    app.run(port=8486, debug=False)
