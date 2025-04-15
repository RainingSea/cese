from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
job_manager = JobManager('jobs.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    jobs = job_manager.get_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password')
            return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect('/')
        else:
            flash('Username already exists.')
    return render_template('registration.html')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        flash('Job posted successfully!')
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/')
    user_profile = user_manager.get_user_profile(session['username'])
    return render_template('profile.html', profile=user_profile)

if __name__ == '__main__':
    app.run(port=8310, debug=False)
