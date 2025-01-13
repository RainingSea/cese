from flask import Flask, render_template, request, redirect, session
from auth import Auth
from profile import Profile
from job import Job

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

auth = Auth()
profile = Profile()
job = Job()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        auth.register(username, password, email)
        return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    jobs = job.load_jobs()
    return render_template('home.html', jobs=jobs)

@app.route('/job_listing')
def job_listing():
    jobs = job.load_jobs()
    return render_template('job_listing.html', jobs=jobs)

@app.route('/job_posting', methods=['GET', 'POST'])
def job_posting():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job.save(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        profile.edit_profile(username, email)
        return redirect('/home')
    user_info = profile.view_profile()
    return render_template('profile.html', user=user_info)

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect('/home')
    return redirect('/')

@app.route('/logout')
def logout_user():
    auth.logout()
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8485, debug=False)
