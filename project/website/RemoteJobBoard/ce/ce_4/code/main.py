from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job
from application import Application

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User().load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('job_listings'))
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/job_post', methods=['GET', 'POST'])
def job_post():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect(url_for('job_listings'))
    return render_template('job_post.html')

@app.route('/job_listings', methods=['GET'])
def job_listings():
    jobs = Job().load_jobs()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', username=session.get('username'))

if __name__ == '__main__':
    app.run(port=8984, debug=False)
