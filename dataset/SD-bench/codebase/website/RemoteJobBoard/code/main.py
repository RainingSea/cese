from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from auth import Auth
from profile import Profile
from job_board import JobBoard

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
job_board = JobBoard()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/browse_jobs')
def browse_jobs():
    jobs = job_board.browse_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job_board.post_job(job)
        return redirect(url_for('browse_jobs'))
    return render_template('post_job.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    user_profile = Profile(username)
    user_info = user_profile.view_profile()
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        user_profile.edit_profile(new_username, new_email)
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user_info)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8312, debug=False)
