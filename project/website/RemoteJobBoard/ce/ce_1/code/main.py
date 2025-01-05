from flask import Flask, render_template, request, redirect, url_for, session
import json
from user import User
from job import Job
from data_storage import DataStorage

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_storage = DataStorage()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        if user.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = data_storage.load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.post_job(title, company, description)
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    user_info = data_storage.load_users()
    return render_template('profile.html', user=user_info.get(username))

if __name__ == '__main__':
    app.run(port=8110, debug=False)
