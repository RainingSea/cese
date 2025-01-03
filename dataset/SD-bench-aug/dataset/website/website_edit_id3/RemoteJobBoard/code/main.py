from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the file
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

# Load jobs from the file
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
    if 'username' in session:
        jobs = load_jobs()
        return render_template('home.html', jobs=jobs)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/job_post', methods=['GET', 'POST'])
def job_post():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect(url_for('home'))
    return render_template('job_post.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        users = load_users()
        current_user = next((user for user in users if user.username == session['username']), None)
        if request.method == 'POST':
            email = request.form['email']
            current_user.email = email
            # Logic to update user profile
            with open('users.txt', 'w') as file:
                for user in users:
                    file.write(f"{user.username}|{user.password}|{user.email}\n")
            return redirect(url_for('home'))
        return render_template('profile.html', username=current_user.username, email=current_user.email)
    return redirect(url_for('login'))

@app.route('/browse_jobs')
def browse_jobs():
    if 'username' in session:
        jobs = load_jobs()
        return render_template('browse_jobs.html', jobs=jobs)
    return redirect(url_for('login'))

@app.route('/apply/<job_title>', methods=['POST'])
def apply(job_title):
    if 'username' in session:
        username = session['username']
        application = Application(username, job_title)
        application.save()
        return redirect(url_for('browse_jobs'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8142, debug=True)
