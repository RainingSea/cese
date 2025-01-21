from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split('|')
            users.append(User(username, password, email))
    return users

def load_jobs():
    jobs = []
    with open('jobs.txt', 'r') as file:
        for line in file:
            title, company, description = line.strip().split('|')
            jobs.append(Job(title, company, description))
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
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/job_listings')
def job_listings():
    jobs = load_jobs()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect(url_for('job_listings'))
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port=8982, debug=False)
