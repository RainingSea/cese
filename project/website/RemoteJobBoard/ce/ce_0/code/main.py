from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        users = DataStorage.load_users()
        if username in users:
            return False
        new_user = User(username, password, email)
        DataStorage.save_user(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        users = DataStorage.load_users()
        return users.get(username) == password

    def update_profile(self, email: str) -> bool:
        # Update the user's email (not implemented in this basic version)
        return True

class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

    def post_job(self, title: str, company: str, description: str) -> bool:
        new_job = Job(title, company, description)
        return DataStorage.save_job(new_job)

    def apply_job(self, username: str) -> bool:
        # Apply for a job (not implemented in this basic version)
        return True

class DataStorage:
    @staticmethod
    def save_user(user: User) -> bool:
        users = DataStorage.load_users()
        users[user.username] = user.password
        with open('users.txt', 'w') as f:
            json.dump(users, f)
        return True

    @staticmethod
    def load_users() -> dict:
        try:
            with open('users.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_job(job: Job) -> bool:
        jobs = DataStorage.load_jobs()
        jobs.append({'title': job.title, 'company': job.company, 'description': job.description})
        with open('jobs.txt', 'w') as f:
            json.dump(jobs, f)
        return True

    @staticmethod
    def load_jobs() -> list:
        try:
            with open('jobs.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password, None)
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
    jobs = DataStorage.load_jobs()
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
    if username:
        users = DataStorage.load_users()
        email = users.get(username)
        return render_template('profile.html', username=username, email=email)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8109, debug=False)
