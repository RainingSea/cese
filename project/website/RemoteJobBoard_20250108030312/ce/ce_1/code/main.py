from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

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
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home', methods=['GET'])
def home():
    jobs = job_manager.get_all_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company_name = request.form['company_name']
        job_description = request.form['job_description']
        job_manager.post_job(job_title, company_name, job_description)
        return redirect(url_for('home'))
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET'])
def profile():
    username = session.get('username')
    user_profile = user_manager.get_user_profile(username)
    return render_template('profile.html', profile=user_profile)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8335, debug=False)
