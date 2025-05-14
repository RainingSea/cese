from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
USERS_FILE = 'users.txt'
JOBS_FILE = 'jobs.txt'

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as f:
        return [line.strip().split('|') for line in f.readlines()]

def save_user(username, password, email):
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}|{password}|{email}|\n")

def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []
    with open(JOBS_FILE, 'r') as f:
        return [line.strip().split('|') for line in f.readlines()]

def save_job(title, company, description, poster):
    job_id = str(len(load_jobs()) + 1)
    with open(JOBS_FILE, 'a') as f:
        f.write(f"{job_id}|{title}|{company}|{description}|{poster}\n")

def update_user_applied_jobs(username, job_id):
    users = load_users()
    updated_users = []
    for user in users:
        if user[0] == username:
            applied_jobs = user[3].split(',') if len(user) > 3 and user[3] else []
            if job_id not in applied_jobs:
                applied_jobs.append(job_id)
                user[3] = ','.join(applied_jobs)
        updated_users.append(user)
    
    with open(USERS_FILE, 'w') as f:
        for user in updated_users:
            f.write('|'.join(user) + '\n')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    jobs = load_jobs()[-3:]  # Show last 3 jobs as featured
    return render_template('home.html', username=session['username'], jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user[0] == username and user[1] == password:
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
        
        users = load_users()
        for user in users:
            if user[0] == username:
                return render_template('register.html', error='Username already exists')
        
        save_user(username, password, email)
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/jobs')
def jobs():
    if 'username' not in session:
        return redirect(url_for('login'))
    all_jobs = load_jobs()
    return render_template('jobs.html', jobs=all_jobs)

@app.route('/apply/<job_id>')
def apply(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    update_user_applied_jobs(session['username'], job_id)
    return redirect(url_for('jobs'))

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        save_job(title, company, description, session['username'])
        return redirect(url_for('home'))
    
    return render_template('post_job.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    jobs = load_jobs()
    user_data = None
    applied_jobs = []
    
    for user in users:
        if user[0] == session['username']:
            user_data = user
            if len(user) > 3 and user[3]:
                applied_job_ids = user[3].split(',')
                applied_jobs = [job for job in jobs if job[0] in applied_job_ids]
            break
    
    return render_template('profile.html', 
                         username=user_data[0], 
                         email=user_data[2], 
                         applied_jobs=applied_jobs)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8042, debug=False)
