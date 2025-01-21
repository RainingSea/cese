from flask import Flask, render_template, request, redirect, url_for, session
from user_management import Auth
from job_management import JobBoard

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Auth.login(username, password):
            return redirect(url_for('home'))
        else:
            return "Login failed. Please check your credentials.", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def registration():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        Auth.register(username, password, email)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/home')
def home():
    """Displays the home page."""
    return render_template('home.html')

@app.route('/browse_jobs')
def browse_jobs():
    """Displays the list of jobs."""
    jobs = JobBoard.browse_jobs()
    return render_template('browse_jobs.html', jobs=jobs)

@app.route('/job/<job_id>', methods=['GET', 'POST'])
def job_detail(job_id: str):
    """Displays the details of a specific job."""
    job = Job.load_by_id(job_id)
    if job is None:
        return "Job not found.", 404
    if request.method == 'POST':
        username = session.get('username')
        if username:
            user = User.load(username)
            user.apply(job_id)
            return redirect(url_for('browse_jobs'))
    return render_template('job_detail.html', job=job)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    """Handles job posting."""
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        JobBoard.post_job(title, company, description)
        return redirect(url_for('browse_jobs'))
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Displays and updates the user's profile."""
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    user = Auth.view_profile(username)
    if request.method == 'POST':
        new_password = request.form['password']
        new_email = request.form['email']
        user.update_profile(new_password, new_email)
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    """Logs out the user."""
    Auth.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8985, debug=False)
