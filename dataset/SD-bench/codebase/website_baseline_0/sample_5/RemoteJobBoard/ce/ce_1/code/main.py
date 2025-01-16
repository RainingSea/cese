from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from profile import Profile

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    job_list = Job().load_jobs()
    return render_template('home.html', jobs=job_list)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.save()
        return redirect(url_for('home'))
    return render_template('job_post.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    user = User().load_users()
    user_profile = Profile(user)
    return render_template('profile.html', profile=user_profile.view_profile())

if __name__ == '__main__':
    app.run(port=8484, debug=False)
