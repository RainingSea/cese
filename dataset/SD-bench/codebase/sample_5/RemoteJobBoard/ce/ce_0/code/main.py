from flask import Flask, render_template, request, redirect, session
from user import User
from job import Job
from job_board import JobBoard

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize JobBoard with file paths
job_board = JobBoard('users.txt', 'jobs.txt', 'applied_jobs.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if job_board.login_user(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if job_board.register_user(username, password, email):
            return redirect('/')
        else:
            return "Registration failed"
    return render_template('register.html')

@app.route('/home')
def home():
    featured_jobs = job_board.get_featured_jobs()
    return render_template('home.html', jobs=featured_jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job_board.post_job(job)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    user_profile = job_board.get_user_profile(username)
    return render_template('profile.html', user=user_profile)

@app.route('/browse_jobs')
def browse_jobs():
    all_jobs = job_board.browse_jobs()
    return render_template('browse_jobs.html', jobs=all_jobs)

if __name__ == '__main__':
    app.run(port=8483, debug=False)
