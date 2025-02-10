from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
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
                title, company, description = line.strip().split('|')
                jobs.append(Job(title, company, description))
    except FileNotFoundError:
        pass
    return jobs

users = load_users()
jobs = load_jobs()

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
        users.append(new_user)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=jobs)

@app.route('/job_listing')
def job_listing():
    return render_template('job_listing.html', jobs=jobs)

@app.route('/job_post', methods=['GET', 'POST'])
def job_post():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        jobs.append(new_job)
        new_job.save()
        return redirect(url_for('job_listing'))
    return render_template('job_post.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', user=session.get('username'))

if __name__ == '__main__':
    app.run(port=8574, debug=False)
