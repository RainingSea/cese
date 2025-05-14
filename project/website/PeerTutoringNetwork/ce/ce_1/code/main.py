from flask import Flask, render_template, redirect, url_for, session, request
from auth import AuthHandler
from tutor import TutorHandler
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

auth_handler = AuthHandler('users.txt')
tutor_handler = TutorHandler('tutors.txt', 'requests.txt')

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_handler.validate_login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if auth_handler.create_user(username, password, email):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/tutors')
def tutors():
    if 'username' not in session:
        return redirect(url_for('login'))
    tutors_list = tutor_handler.get_all_tutors()
    return render_template('tutors.html', tutors=tutors_list)

@app.route('/request', methods=['GET', 'POST'])
def request_tutor():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        date = request.form['date']
        if tutor_handler.create_request(session['username'], subject, details, date):
            return redirect(url_for('dashboard'))
        return render_template('request.html', error='Request failed')
    return render_template('request.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_info = auth_handler.get_user_info(session['username'])
    return render_template('profile.html', user=user_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('contacts.txt', 'a') as f:
            f.write(f"{len(open('contacts.txt').readlines()) + 1}|{name}|{email}|{message}|{timestamp}\n")
        return redirect(url_for('dashboard'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8029, debug=False)
