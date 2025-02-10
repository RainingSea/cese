from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from job_manager import JobManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
            return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = job_manager.get_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job_manager.post_job(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/job_listing')
def job_listing():
    jobs = job_manager.get_jobs()
    return render_template('job_listing.html', jobs=jobs)

if __name__ == '__main__':
    app.run(port=8575, debug=False)
