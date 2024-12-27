from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from JobManager import JobManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
            return "Login Failed. Please check your credentials."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration Failed. Username may already exist."
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/job_post', methods=['GET', 'POST'])
def job_post():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company_name = request.form['company_name']
        job_description = request.form['job_description']
        if job_manager.post_job(job_title, company_name, job_description):
            return redirect(url_for('job_listings'))
        else:
            return "Job posting failed."
    return render_template('job_post.html')

@app.route('/job_listings')
def job_listings():
    jobs = job_manager.get_all_jobs()
    return render_template('job_listings.html', jobs=jobs)

@app.route('/apply/<int:job_id>')
def apply(job_id):
    username = session.get('username')
    if username:
        if job_manager.apply_for_job(username, job_id):
            return redirect(url_for('job_listings'))
        else:
            return "Application failed."
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    user_profile = user_manager.get_user_profile(username)

    if request.method == 'POST':
        new_password = request.form['password']
        user_manager.update_user_profile(username, new_password)
        return redirect(url_for('profile'))

    return render_template('profile.html', user_profile=user_profile)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)