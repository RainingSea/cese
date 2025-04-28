from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def get_user_profile(self, username: str) -> dict:
        for user in self.users:
            if user[0] == username:
                return {'username': user[0]}
        return {}

    def edit_profile(self, username: str, new_data: dict) -> bool:
        for user in self.users:
            if user[0] == username:
                user[0] = new_data.get('username', user[0])
                self.save_users()
                return True
        return False

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user[0]}|{user[1]}\n")

class JobManager:
    def __init__(self):
        self.jobs = self.load_jobs()

    def load_jobs(self):
        if not os.path.exists('jobs.txt'):
            return []
        with open('jobs.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def post_job(self, job_details: dict) -> bool:
        self.jobs.append([job_details['title'], job_details['description'], job_details['company']])
        with open('jobs.txt', 'a') as file:
            file.write(f"{job_details['title']}|{job_details['description']}|{job_details['company']}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        if 0 <= job_id < len(self.jobs):
            with open('applied_jobs.txt', 'a') as file:
                file.write(f"{username}|{job_id}\n")
            return True
        return False

user_manager = UserManager()
job_manager = JobManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/home')
    return "Login failed", 400

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template('home.html', jobs=job_manager.get_all_jobs())

@app.route('/post_job', methods=['POST'])
def post_job():
    if 'username' not in session:
        return redirect('/')
    job_details = {
        'title': request.form['title'],
        'description': request.form['description'],
        'company': request.form['company']
    }
    job_manager.post_job(job_details)
    return redirect('/home')

@app.route('/browse_jobs')
def browse_jobs():
    if 'username' not in session:
        return redirect('/')
    return render_template('browse_jobs.html', jobs=job_manager.get_all_jobs())

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/')
    user_profile = user_manager.get_user_profile(session.get('username'))
    return render_template('profile.html', profile=user_profile)

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'username' not in session:
        return redirect('/')
    new_data = {
        'username': request.form['username']
    }
    user_manager.edit_profile(session['username'], new_data)
    return redirect('/profile')

@app.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    if job_manager.apply_for_job(username, job_id):
        return redirect('/browse_jobs')
    return "Job application failed", 400

if __name__ == '__main__':
    app.run(port=8409, debug=False)
