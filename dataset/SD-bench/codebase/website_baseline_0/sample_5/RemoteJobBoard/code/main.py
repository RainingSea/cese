from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as file:
            file.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_all():
        jobs = []
        with open('jobs.txt', 'r') as file:
            for line in file:
                job_data = line.strip().split('|')
                jobs.append(Job(job_data[0], job_data[1], job_data[2]))
        return jobs

    @staticmethod
    def load_by_title(title: str):
        with open('jobs.txt', 'r') as file:
            for line in file:
                job_data = line.strip().split('|')
                if job_data[0] == title:
                    return Job(job_data[0], job_data[1], job_data[2])
        return None

class Application:
    def __init__(self, username: str, job_title: str):
        self.username = username
        self.job_title = job_title

    def save(self):
        with open('applications.txt', 'a') as file:
            file.write(f"{self.username}|{self.job_title}\n")

class Auth:
    @staticmethod
    def login(username: str, password: str) -> bool:
        user = User.load(username)
        return user is not None and user.password == password

    @staticmethod
    def register(username: str, password: str, email: str) -> bool:
        if User.load(username) is None:
            new_user = User(username, password, email)
            new_user.save()
            return True
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Auth.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Auth.register(username, password, email):
            return redirect('/')
        else:
            return "User already exists", 400
    return render_template('register.html')

@app.route('/home')
def home():
    jobs = Job.load_all()
    if not jobs:
        return "No job listings available", 404
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect('/home')
    return render_template('job_post.html')

@app.route('/apply_job/<job_title>', methods=['POST'])
def apply_job(job_title):
    username = session.get('username')
    if username:
        application = Application(username, job_title)
        application.save()
        return redirect('/home')
    return "You must be logged in to apply for jobs", 403

@app.route('/profile')
def profile():
    username = session.get('username')
    user = User.load(username)
    if user is None:
        return "User not found", 404
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8488, debug=False)
