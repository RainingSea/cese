from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from profile import Profile
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
user = User()
job = Job()
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

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job.save(title, company, description)
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile')
def user_profile():
    user_info = profile.view_profile()
    return render_template('profile.html', user_info=user_info)

@app.route('/job_listings')
def job_listings():
    jobs = job.load_jobs()
    return render_template('job_listings.html', jobs=jobs)

if __name__ == '__main__':
    app.run(port=8980, debug=False)
