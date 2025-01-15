from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_all():
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    @staticmethod
    def validate_credentials(username: str, password: str) -> bool:
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_all():
        jobs = []
        try:
            with open('jobs.txt', 'r') as f:
                for line in f:
                    title, company, description = line.strip().split('|')
                    jobs.append(Job(title, company, description))
        except FileNotFoundError:
            pass
        return jobs

class Application:
    def __init__(self, username: str, job_title: str):
        self.username = username
        self.job_title = job_title

    def save(self):
        with open('applied_jobs.txt', 'a') as f:
            f.write(f"{self.username}|{self.job_title}\n")

    @staticmethod
    def load_all():
        applications = []
        try:
            with open('applied_jobs.txt', 'r') as f:
                for line in f:
                    username, job_title = line.strip().split('|')
                    applications.append(Application(username, job_title))
        except FileNotFoundError:
            pass
        return applications

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.validate_credentials(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid login credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        user.save()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    jobs = Job.load_all()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.save()
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/apply/<job_title>', methods=['POST'])
def apply(job_title):
    if 'username' not in session:
        return redirect(url_for('login'))
    application = Application(session['username'], job_title)
    application.save()
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Here you can implement profile editing logic
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8075, debug=False)
