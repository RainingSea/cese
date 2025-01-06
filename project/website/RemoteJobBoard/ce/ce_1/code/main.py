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
            f.write(json.dumps(self.__dict__) + '\n')

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = json.loads(line.strip())
                if user_data['username'] == username:
                    return User(**user_data)
        return None

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as f:
            f.write(json.dumps(self.__dict__) + '\n')

    @staticmethod
    def load_all():
        jobs = []
        with open('jobs.txt', 'r') as f:
            for line in f:
                job_data = json.loads(line.strip())
                jobs.append(Job(**job_data))
        return jobs

@app.route('/')
def login():
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
    return render_template('home.html', jobs=Job.load_all())

@app.route('/browse_jobs')
def browse_jobs():
    return render_template('browse_jobs.html', jobs=Job.load_all())

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job = Job(title, company, description)
        job.save()
        return redirect(url_for('home'))
    return render_template('post_job.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port=8191, debug=False)
