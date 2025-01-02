from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        users = []
        user_exists = False
        # Load all existing users
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    users.append(f"{self.username}|{self.password}|{self.email}\n")  # Update user
                    user_exists = True
                else:
                    users.append(line)  # Keep existing user

        # If user does not exist, add it
        if not user_exists:
            users.append(f"{self.username}|{self.password}|{self.email}\n")

        # Write back to the file
        with open('users.txt', 'w') as f:
            f.writelines(users)

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1], user_data[2])
        return None

class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_all():
        jobs = []
        with open('jobs.txt', 'r') as f:
            for line in f:
                job_data = line.strip().split('|')
                jobs.append(Job(job_data[0], job_data[1], job_data[2]))
        return jobs

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.load(username)
        if user and user.password == password:
            session['username'] = username
            return redirect('/home')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        jobs = Job.load_all()
        return render_template('home.html', jobs=jobs)
    return redirect('/')

@app.route('/browse_jobs')
def browse_jobs():
    jobs = Job.load_all()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        new_job = Job(title, company, description)
        new_job.save()
        return redirect('/home')
    return render_template('post_job.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect('/')
    user = User.load(session['username'])
    if request.method == 'POST':
        user.email = request.form['email']
        user.save()
        return redirect('/profile')
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8184, debug=True)
