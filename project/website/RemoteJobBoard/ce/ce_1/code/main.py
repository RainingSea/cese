from flask import Flask, render_template, request, redirect, session, flash
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

user_manager = UserManager()
job_manager = JobManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login_user(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password.')
            return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register_user(username, password):
            flash('Registration successful. Please log in.')
            return redirect('/')
        else:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    jobs = job_manager.get_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.add_job(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('You need to log in first.')
        return redirect('/')
    username = session.get('username')
    user_profile = user_manager.get_user_profile(username)
    return render_template('profile.html', profile=user_profile)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect('/')

if __name__ == '__main__':
    user_manager.load_users()
    job_manager.load_jobs()
    app.run(port=8308, debug=False)
