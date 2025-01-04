from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from job import Job
from application import Application  # Import the Application class

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from the file
def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
    except Exception as e:
        print(f"Error loading users: {e}")
    return users

# Load jobs from the file
def load_jobs():
    jobs = []
    try:
        with open('jobs.txt', 'r') as file:
            for line in file:
                title, company, description = line.strip().split('|')
                jobs.append(Job(title, company, description))
    except Exception as e:
        print(f"Error loading jobs: {e}")
    return jobs

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
        return "Invalid credentials. Please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()  # Save user to the file
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    jobs = load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/browse_jobs')
def browse_jobs():
    jobs = load_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()  # Save job to the file
        return redirect(url_for('home'))
    
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    users = load_users()
    current_user = next((user for user in users if user.username == session['username']), None)

    if request.method == 'POST':
        new_email = request.form['email']
        current_user.email = new_email
        # Save updated user info
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")
        return redirect(url_for('profile'))

    return render_template('profile.html', user=current_user)

@app.route('/apply_job/<job_title>', methods=['POST'])
def apply_job(job_title):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    application = Application(username, job_title)
    application.save()  # Save application to the file
    return redirect(url_for('browse_jobs'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)