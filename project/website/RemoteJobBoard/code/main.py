from flask import Flask, render_template, request, redirect, session, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        users = DataStorage.load_users()
        if username in [user['username'] for user in users]:
            return False
        new_user = User(username, password, email)
        DataStorage.save_user(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        users = DataStorage.load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return True
        return False

    def update_profile(self, email: str) -> bool:
        users = DataStorage.load_users()
        for user in users:
            if user['username'] == self.username:
                user['email'] = email
                DataStorage.save_users(users)
                return True
        return False

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def post_job(self, title: str, company: str, description: str) -> bool:
        new_job = Job(title, company, description)
        return DataStorage.save_job(new_job)

    def apply_job(self, username: str) -> bool:
        applied_jobs = DataStorage.load_applied_jobs(username)
        if self.title not in applied_jobs:
            DataStorage.save_applied_job(username, self.title)
            return True
        return False

class DataStorage:
    @staticmethod
    def save_user(user: User) -> bool:
        users = DataStorage.load_users()
        users.append({'username': user.username, 'password': user.password, 'email': user.email})
        with open('users.txt', 'w') as f:
            json.dump(users, f)
        return True

    @staticmethod
    def load_users() -> list:
        try:
            with open('users.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

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

    @staticmethod
    def save_applied_job(username: str, job_title: str) -> bool:
        applied_jobs = DataStorage.load_applied_jobs(username)
        applied_jobs.append(job_title)
        with open('applied_jobs.txt', 'w') as f:
            json.dump({username: applied_jobs}, f)
        return True

    @staticmethod
    def load_applied_jobs(username: str) -> list:
        try:
            with open('applied_jobs.txt', 'r') as f:
                data = json.load(f)
                return data.get(username, [])
        except FileNotFoundError:
            return []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password, '')
        if user.login(username, password):
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
    users = DataStorage.load_users()
    user_info = next((user for user in users if user['username'] == username), None)
    return render_template('profile.html', user=user_info)

if __name__ == '__main__':
    app.run(port=8111, debug=False)
