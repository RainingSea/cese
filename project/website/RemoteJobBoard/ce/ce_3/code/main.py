from flask import Flask, render_template, redirect, request, session
from auth import Auth
from user import User
from job import Job

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
user = User()
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
        if auth.register(username, password, email):
            return redirect('/')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html', jobs=job.load_all())

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        job.save(title, company, description)
        return redirect('/home')
    return render_template('job_posting.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', user=user.load(session['username']))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if auth.login(username, password):
        session['username'] = username
        return redirect('/home')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8983, debug=False)
