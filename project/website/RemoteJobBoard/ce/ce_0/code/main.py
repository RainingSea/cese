from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from job_manager import JobManager
from application_manager import ApplicationManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
job_manager = JobManager()
application_manager = ApplicationManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def user_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/login')
        else:
            return render_template('registration.html', error="Username already exists.")
    return render_template('registration.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    jobs = job_manager.get_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    user_manager.load_users()
    job_manager.load_jobs()
    application_manager.load_applications()
    app.run(port=8306, debug=False)
