from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def register(self, username: str, password: str, email: str) -> bool:
        if self.username_exists(username):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

    def edit_profile(self, username: str, password: str, email: str) -> None:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == self.username:
                    users.append(f"{username}|{password}|{email}\n")
                else:
                    users.append(line)
        with open('users.txt', 'w') as f:
            f.writelines(users)

    def apply_job(self, job_id: str) -> None:
        self.applied_jobs.append(job_id)

    @staticmethod
    def username_exists(username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip().split('|')[0] == username:
                    return True
        return False


class Job:
    def __init__(self, job_id: str, title: str, company: str, description: str):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.description = description

    def post_job(self, title: str, company: str, description: str) -> None:
        job_id = str(len(self.get_jobs()) + 1)
        with open('jobs.txt', 'a') as f:
            f.write(f"{job_id}|{title}|{company}|{description}\n")

    @staticmethod
    def get_jobs() -> list:
        jobs = []
        with open('jobs.txt', 'r') as f:
            for line in f:
                job_data = line.strip().split('|')
                jobs.append(Job(job_data[0], job_data[1], job_data[2], job_data[3]))
        return jobs


class Main:
    def __init__(self):
        self.user = None
        self.job = Job("", "", "", "")

    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User(username, password, "")
            if user.login(username, password):
                session['username'] = username
                return redirect('/home')
            else:
                flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            user = User(username, password, email)
            if user.register(username, password, email):
                flash('Registration successful!')
                return redirect('/')
            else:
                flash('Username already exists!')
        return render_template('registration.html')

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/job_listing')
    def job_listing():
        jobs = Job.get_jobs()
        return render_template('job_listing.html', jobs=jobs)

    @app.route('/post_job', methods=['GET', 'POST'])
    def post_job():
        if request.method == 'POST':
            title = request.form['title']
            company = request.form['company']
            description = request.form['description']
            job = Job("", title, company, description)
            job.post_job(title, company, description)
            flash('Job posted successfully!')
            return redirect('/job_listing')
        return render_template('job_posting.html')

    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            user = User(session['username'], password, email)
            user.edit_profile(username, password, email)
            flash('Profile updated successfully!')
            return redirect('/profile')
        return render_template('profile.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')

    def main(self):
        app.run(port=8237, debug=False)

if __name__ == '__main__':
    main = Main()
    main.main()