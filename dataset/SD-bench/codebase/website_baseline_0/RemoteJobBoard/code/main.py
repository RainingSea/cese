from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from auth import Auth
from profile import Profile

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and jobs from files
users = User.load_users()
jobs = Job.load_jobs()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if Auth.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        Job(title, company, description).save()
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    user_info = Profile.view_profile(username)
    return render_template('profile.html', user_info=user_info)

@app.route('/browse_jobs')
def browse_jobs():
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/apply_job/<job_title>', methods=['POST'])
def apply_job(job_title):
    username = session.get('username')
    if username:
        Profile.apply_job(username, job_title)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8551, debug=False)
