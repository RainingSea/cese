from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from auth import Auth
from profile import Profile

app = Flask(__name__)
app.secret_key = 'supersecretkey'

auth = Auth()
profile = Profile()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/browse_jobs')
def browse_jobs():
    jobs = Job.load_all()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.save()
        return redirect(url_for('browse_jobs'))
    return render_template('job_posting.html')

@app.route('/profile')
def user_profile():
    user_info = profile.view_profile()
    return render_template('profile.html', user=user_info)

if __name__ == '__main__':
    app.run(port=8577, debug=False)
