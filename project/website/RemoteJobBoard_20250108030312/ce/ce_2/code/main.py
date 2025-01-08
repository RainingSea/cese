from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
job_manager = JobManager('jobs.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Login failed. Please check your credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username may already exist."
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = job_manager.get_all_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company_name = request.form['company_name']
        job_description = request.form['job_description']
        if job_manager.post_job(job_title, company_name, job_description):
            return redirect(url_for('home'))
        else:
            return "Job posting failed."
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    username = session.get('username')
    user_profile = user_manager.get_user_profile(username)
    return render_template('profile.html', profile=user_profile)

if __name__ == '__main__':
    app.run(port=8336, debug=False)
