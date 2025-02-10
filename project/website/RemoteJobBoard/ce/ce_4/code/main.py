from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
job_manager = JobManager('jobs.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register_user(username, password, email):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', jobs=job_manager.get_all_jobs())

@app.route('/browse_jobs', methods=['GET'])
def browse_jobs():
    return render_template('browse_jobs.html', jobs=job_manager.get_all_jobs())

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        return redirect(url_for('home'))
    return render_template('job_post.html')

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(port=8578, debug=False)
