from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key_for_demo'

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        self._load_users()

    def _load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}

    def register(self, username, password, email):
        if username in self.users:
            return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        self.users[username] = {'password': password, 'email': email}
        return True

    def login(self, username, password):
        user = self.users.get(username)
        return user and user['password'] == password

    def get_user(self, username):
        return self.users.get(username)

    def update_user(self, username, new_data):
        if username not in self.users:
            return False
        self.users[username].update(new_data)
        with open(self.users_file, 'w') as f:
            for uname, data in self.users.items():
                f.write(f"{uname}|{data['password']}|{data['email']}\n")
        return True

class JobManager:
    def __init__(self):
        self.jobs_file = 'jobs.txt'
        self._load_jobs()

    def _load_jobs(self):
        self.jobs = {}
        if os.path.exists(self.jobs_file):
            with open(self.jobs_file, 'r') as f:
                for line in f:
                    job_id, title, company, description, poster = line.strip().split('|')
                    self.jobs[job_id] = {
                        'title': title,
                        'company': company,
                        'description': description,
                        'poster': poster
                    }

    def post_job(self, title, company, description, poster):
        job_id = str(len(self.jobs) + 1)
        with open(self.jobs_file, 'a') as f:
            f.write(f"{job_id}|{title}|{company}|{description}|{poster}\n")
        self.jobs[job_id] = {
            'title': title,
            'company': company,
            'description': description,
            'poster': poster
        }
        return True

    def get_all_jobs(self):
        return self.jobs

    def get_job(self, job_id):
        return self.jobs.get(job_id)

class ApplicationManager:
    def __init__(self):
        self.apps_file = 'applications.txt'
        self._load_applications()

    def _load_applications(self):
        self.applications = []
        if os.path.exists(self.apps_file):
            with open(self.apps_file, 'r') as f:
                for line in f:
                    username, job_id = line.strip().split('|')
                    self.applications.append({'username': username, 'job_id': job_id})

    def apply(self, username, job_id):
        with open(self.apps_file, 'a') as f:
            f.write(f"{username}|{job_id}\n")
        self.applications.append({'username': username, 'job_id': job_id})
        return True

    def get_user_applications(self, username):
        return [app for app in self.applications if app['username'] == username]

user_manager = UserManager()
job_manager = JobManager()
app_manager = ApplicationManager()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    jobs = job_manager.get_all_jobs()
    featured_jobs = dict(list(jobs.items())[:3])
    return render_template('home.html', username=session['username'], jobs=featured_jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/browse_jobs')
def browse_jobs():
    if 'username' not in session:
        return redirect(url_for('login'))
    jobs = job_manager.get_all_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description, session['username'])
        return redirect(url_for('home'))
    return render_template('post_job.html')

@app.route('/apply_job/<job_id>')
def apply_job(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    app_manager.apply(session['username'], job_id)
    return redirect(url_for('browse_jobs'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = user_manager.get_user(session['username'])
    applications = app_manager.get_user_applications(session['username'])
    applied_jobs = []
    for app in applications:
        job = job_manager.get_job(app['job_id'])
        if job:
            applied_jobs.append(job)
    return render_template('profile.html', user=user, applied_jobs=applied_jobs)

if __name__ == '__main__':
    app.run(port=8041, debug=False)
