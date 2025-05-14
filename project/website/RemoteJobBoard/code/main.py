from flask import Flask, render_template, request, redirect, url_for, session
import os
import logging
import tempfile
import atexit

app = Flask(__name__)
app.secret_key = 'secret_key'
logging.basicConfig(level=logging.DEBUG)

class UserManager:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.users_file = 'test_users.txt' if test_mode else 'users.txt'
        self._load_users()

    def _load_users(self):
        self.users = {}
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 3:
                            self.users[parts[0]] = {
                                'password': parts[1],
                                'email': parts[2]
                            }
        except IOError as e:
            logging.error(f"Error loading users: {e}")

    def register(self, username, password, email):
        if username in self.users:
            return False
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username}|{password}|{email}\n")
            self.users[username] = {'password': password, 'email': email}
            return True
        except IOError as e:
            logging.error(f"Error registering user: {e}")
            return False

    def login(self, username, password):
        user = self.users.get(username)
        if user and user['password'] == password:
            logging.debug(f"Successful login for user: {username}")
            return True
        logging.debug(f"Failed login attempt for user: {username}")
        return False

    def get_user(self, username):
        return self.users.get(username)

    def update_user(self, username, email=None, password=None):
        if username not in self.users:
            return False
        try:
            if email:
                self.users[username]['email'] = email
            if password:
                self.users[username]['password'] = password
            
            with open(self.users_file, 'w') as f:
                for uname, data in self.users.items():
                    f.write(f"{uname}|{data['password']}|{data['email']}\n")
            return True
        except IOError as e:
            logging.error(f"Error updating user: {e}")
            return False

class JobManager:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.jobs_file = 'test_jobs.txt' if test_mode else 'jobs.txt'
        self._load_jobs()

    def _load_jobs(self):
        self.jobs = []
        self.next_id = 1
        try:
            if os.path.exists(self.jobs_file):
                with open(self.jobs_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 5:
                            self.jobs.append({
                                'id': parts[0],
                                'title': parts[1],
                                'company': parts[2],
                                'description': parts[3],
                                'poster': parts[4]
                            })
                            self.next_id = max(self.next_id, int(parts[0]) + 1)
        except IOError as e:
            logging.error(f"Error loading jobs: {e}")

    def create_job(self, title, company, description, poster):
        job_id = str(self.next_id)
        try:
            with open(self.jobs_file, 'a') as f:
                f.write(f"{job_id}|{title}|{company}|{description}|{poster}\n")
            self.jobs.append({
                'id': job_id,
                'title': title,
                'company': company,
                'description': description,
                'poster': poster
            })
            self.next_id += 1
            return job_id
        except IOError as e:
            logging.error(f"Error creating job: {e}")
            return None

    def get_jobs(self):
        return self.jobs

    def get_job(self, job_id):
        for job in self.jobs:
            if job['id'] == job_id:
                return job
        return None

class ApplicationManager:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.applications_file = 'test_applications.txt' if test_mode else 'applications.txt'
        self._load_applications()

    def _load_applications(self):
        self.applications = []
        try:
            if os.path.exists(self.applications_file):
                with open(self.applications_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 2:
                            self.applications.append({
                                'job_id': parts[0],
                                'username': parts[1]
                            })
        except IOError as e:
            logging.error(f"Error loading applications: {e}")

    def apply(self, job_id, username):
        for app in self.applications:
            if app['job_id'] == job_id and app['username'] == username:
                return False
        try:
            with open(self.applications_file, 'a') as f:
                f.write(f"{job_id}|{username}\n")
            self.applications.append({
                'job_id': job_id,
                'username': username
            })
            return True
        except IOError as e:
            logging.error(f"Error applying for job: {e}")
            return False

    def get_applications(self, username):
        return [app['job_id'] for app in self.applications if app['username'] == username]

def create_test_files():
    with open('test_users.txt', 'w') as f:
        f.write("testuser|testpass|test@example.com\n")
    with open('test_jobs.txt', 'w') as f:
        f.write("1|Test Job|Test Company|Test Description|testuser\n")
    with open('test_applications.txt', 'w') as f:
        f.write("1|testuser\n")

def cleanup_test_files():
    for f in ['test_users.txt', 'test_jobs.txt', 'test_applications.txt']:
        try:
            os.remove(f)
        except:
            pass

test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
if test_mode:
    create_test_files()
    atexit.register(cleanup_test_files)

user_manager = UserManager(test_mode)
job_manager = JobManager(test_mode)
application_manager = ApplicationManager(test_mode)

@app.route('/')
def login_route():
    if 'username' in session:
        return redirect(url_for('home_route'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        logging.debug(f"Session set for user: {username}")
        return redirect(url_for('home_route'))
    return render_template('login.html', error='Invalid credentials')

@app.route('/register')
def register_route():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    if user_manager.register(username, password, email):
        session['username'] = username
        return redirect(url_for('home_route'))
    return render_template('register.html', error='Username already exists')

@app.route('/home')
def home_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    jobs = job_manager.get_jobs()
    featured_jobs = jobs[-3:] if len(jobs) > 3 else jobs
    return render_template('home.html', username=session['username'], jobs=featured_jobs)

@app.route('/jobs')
def jobs_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    jobs = job_manager.get_jobs()
    applications = application_manager.get_applications(session['username'])
    return render_template('jobs.html', jobs=jobs, applications=applications)

@app.route('/post_job')
def post_job_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    return render_template('post_job.html')

@app.route('/post_job', methods=['POST'])
def post_job_post():
    title = request.form['title']
    company = request.form['company']
    description = request.form['description']
    job_manager.create_job(title, company, description, session['username'])
    return redirect(url_for('jobs_route'))

@app.route('/profile')
def profile_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    user = user_manager.get_user(session['username'])
    applications = application_manager.get_applications(session['username'])
    jobs = []
    for job_id in applications:
        job = job_manager.get_job(job_id)
        if job:
            jobs.append(job)
    return render_template('profile.html', user=user, jobs=jobs)

@app.route('/edit_profile')
def edit_profile_route():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    user = user_manager.get_user(session['username'])
    return render_template('edit_profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login_route'))
    username = session['username']
    email = request.form.get('email')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    
    success = True
    if email:
        success = user_manager.update_user(username, email=email)
    if new_password:
        user = user_manager.get_user(username)
        if user and user['password'] == current_password:
            success = success and user_manager.update_user(username, password=new_password)
        else:
            success = False
    
    if success:
        return redirect(url_for('profile_route'))
    return redirect(url_for('edit_profile_route', error='Failed to update profile'))

@app.route('/apply/<job_id>')
def apply_route(job_id):
    if 'username' not in session:
        return redirect(url_for('login_route'))
    application_manager.apply(job_id, session['username'])
    return redirect(url_for('jobs_route'))

@app.route('/logout')
def logout_route():
    session.pop('username', None)
    return redirect(url_for('login_route'))

@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=8044, debug=False)
