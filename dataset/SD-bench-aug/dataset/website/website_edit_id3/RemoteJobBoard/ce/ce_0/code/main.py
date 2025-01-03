from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
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

# Load jobs from file
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

# Load applications from file
def load_applications():
    applications = []
    try:
        with open('applied_jobs.txt', 'r') as file:
            for line in file:
                username, job_title = line.strip().split('|')
                applications.append(Application(username, job_title))
    except FileNotFoundError:
        pass
    return applications

# Home route
@app.route('/')
def home():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        jobs = load_jobs()
        return render_template('home.html', jobs=jobs)
    return redirect(url_for('login'))

# Registration route
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

# Job posting route
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect(url_for('dashboard'))
    return render_template('job_post.html')

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        users = load_users()
        current_user = next((user for user in users if user.username == session['username']), None)
        if request.method == 'POST':
            current_user.email = request.form['email']
            current_user.save()
            return redirect(url_for('dashboard'))
        return render_template('profile.html', username=current_user.username, email=current_user.email)
    return redirect(url_for('login'))

# Browse jobs route
@app.route('/browse_jobs')
def browse_jobs():
    jobs = load_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

# Apply for job route
@app.route('/apply/<job_title>', methods=['POST'])
def apply(job_title):
    if 'username' in session:
        application = Application(session['username'], job_title)
        application.save()
        return redirect(url_for('browse_jobs'))
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8141, debug=True)
