from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from job import Job

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and jobs from files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_jobs():
    jobs = []
    with open('jobs.txt', 'r') as file:
        for line in file:
            title, company, description = line.strip().split('|')
            jobs.append(Job(title, company, description))
    return jobs

users = load_users()
jobs = load_jobs()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        jobs.append(new_job)
        with open('jobs.txt', 'a') as file:
            file.write(f"{title}|{company}|{description}\n")
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        for user in users:
            if user.username == session.get('username'):
                user.username = new_username
                user.password = new_password
                break
        # Update the users.txt file
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")
        session['username'] = new_username
        return redirect(url_for('profile'))
    return render_template('profile.html', username=session.get('username'))

@app.route('/browse_jobs')
def browse_jobs():
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    job = jobs[job_id]
    username = session['username']
    # Here you would typically save the application to a database or file
    # For simplicity, we will just print it
    print(f"{username} applied for {job.title} at {job.company}")
    
    return redirect(url_for('browse_jobs'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8463, debug=False)
