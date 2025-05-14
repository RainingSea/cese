from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # For session management

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# File paths
USERS_FILE = 'users.txt'
JOBS_FILE = 'jobs.txt'
APPLICATIONS_FILE = 'applications.txt'

# Helper functions
def validate_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3 and parts[0] == username and parts[2] == password:
                return True
    return False

def create_user(username, email, password):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == username:
                    return False
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username},{email},{password}\n")
    return True

def get_jobs():
    jobs = []
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 4:
                    job = {
                        'id': parts[0],
                        'title': parts[1],
                        'company': parts[2],
                        'description': parts[3],
                        'poster': parts[4] if len(parts) > 4 else ''
                    }
                    jobs.append(job)
    return jobs

def add_job(title, company, description, poster):
    job_id = str(len(get_jobs()) + 1)
    with open(JOBS_FILE, 'a') as f:
        f.write(f"{job_id},{title},{company},{description},{poster}\n")
    return True

def apply_to_job(job_id, username):
    with open(APPLICATIONS_FILE, 'a') as f:
        f.write(f"{job_id},{username}\n")
    return True

def get_user_data(username):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == username:
                    return {'username': parts[0], 'email': parts[1]}
    return None

def update_user_data(username, email):
    users = []
    updated = False
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[0] == username:
                    users.append(f"{username},{email},{parts[2]}\n")
                    updated = True
                else:
                    users.append(line)
    if updated:
        with open(USERS_FILE, 'w') as f:
            f.writelines(users)
        return True
    return False

def get_user_applications(username):
    applications = []
    if os.path.exists(APPLICATIONS_FILE):
        with open(APPLICATIONS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if parts[1] == username:
                    applications.append(parts[0])
    return applications

# Routes
@app.route('/')
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if validate_user(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html', error="Invalid credentials")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if create_user(username, email, password):
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('register.html', error="Username already exists")

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    jobs = get_jobs()[:3]  # Show first 3 jobs as featured
    return render_template('home.html', username=session['username'], jobs=jobs)

@app.route('/jobs')
def jobs():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('jobs.html', jobs=get_jobs(), username=session['username'])

@app.route('/post_job', methods=['POST'])
def post_job():
    if 'username' not in session:
        return redirect(url_for('login'))
    title = request.form.get('title')
    company = request.form.get('company')
    description = request.form.get('description')
    add_job(title, company, description, session['username'])
    return redirect(url_for('jobs'))

@app.route('/apply_job/<job_id>')
def apply_job(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    apply_to_job(job_id, session['username'])
    return redirect(url_for('jobs'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_data = get_user_data(session['username'])
    applications = get_user_applications(session['username'])
    applied_jobs = [job for job in get_jobs() if job['id'] in applications]
    return render_template('profile.html', user=user_data, applied_jobs=applied_jobs)

@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    email = request.form.get('email')
    if update_user_data(session['username'], email):
        return redirect(url_for('profile'))
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8043, debug=False)
