from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from job_manager import JobManager
from application_manager import ApplicationManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
user_manager = UserManager('users.txt')
job_manager = JobManager('jobs.txt')
application_manager = ApplicationManager('applications.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.')
            return redirect('/')
        else:
            flash('Username already exists. Please choose another.')
    return render_template('registration.html')

@app.route('/home')
def home():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    jobs = job_manager.get_all_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/home')
    flash('Invalid username or password.')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        job_manager.post_job({'title': title, 'description': description})
        flash('Job posted successfully!')
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/browse_jobs')
def browse_jobs():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    jobs = job_manager.get_all_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/apply_job/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    username = session['username']
    if application_manager.record_application(username, job_id):
        flash('Application submitted successfully.')
    else:
        flash('Failed to submit application.')
    return redirect('/browse_jobs')

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    username = session['username']
    user_profile = user_manager.get_user_profile(username)
    return render_template('profile.html', user=user_profile)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    username = session['username']
    if request.method == 'POST':
        new_data = {
            'username': request.form['username'],
            'email': request.form['email']
        }
        user_manager.edit_profile(username, new_data)
        flash('Profile updated successfully.')
        return redirect('/profile')
    return render_template('edit_profile.html', user=user_manager.get_user_profile(username))

if __name__ == '__main__':
    app.run(port=8314, debug=False)
