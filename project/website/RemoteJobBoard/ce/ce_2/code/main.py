from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and jobs from files
users = User.load_users()
jobs = Job.load_jobs()

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

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port=8576, debug=False)
