from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from request_manager import TutoringRequestManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
request_manager = TutoringRequestManager('requests.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/view_tutors')
def view_tutors():
    return render_template('view_tutors.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        date = request.form['date']
        request_manager.create_request(subject, details, date)
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        user_profile = user_manager.get_user_profile(session['username'])
        return render_template('profile.html', user=user_profile)
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(port=8390, debug=False)
