from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Load users and jobs from files
users = User.load_users()
jobs = Job.load_jobs()
applications = Application.load_applications()

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
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=jobs)

@app.route('/browse_jobs')
def browse_jobs():
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        current_user = next((user for user in users if user.username == session['username']), None)
        if request.method == 'POST':
            current_user.email = request.form['email']
            current_user.save()
            return redirect(url_for('profile'))
        user_applications = [app.job_title for app in applications if app.username == current_user.username]
        return render_template('profile.html', user=current_user, applied_jobs=user_applications)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/apply/<job_title>', methods=['POST'])
def apply(job_title):
    if 'username' in session:
        username = session['username']
        new_application = Application(username, job_title)
        new_application.save()
        return redirect(url_for('browse_jobs'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)