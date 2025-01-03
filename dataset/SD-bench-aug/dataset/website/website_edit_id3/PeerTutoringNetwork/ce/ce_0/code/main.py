from flask import Flask, render_template, request, redirect, url_for, session
from file_manager import FileManager
from user import User
from tutor import Tutor
from tutoring_request import TutoringRequest

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
file_manager = FileManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_user = User(username, password, email)
        file_manager.save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tutors = file_manager.load_tutors()
    if request.method == 'POST':
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        username = session['username']
        request_tutoring = TutoringRequest(subject, details, preferred_date, username)
        file_manager.save_tutoring_request(request_tutoring)
    
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    users = file_manager.load_users()
    user_info = next((user for user in users if user.username == username), None)
    
    return render_template('profile.html', user=user_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_messages.txt', 'a') as f:
            f.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = file_manager.load_users()
    user = next((user for user in users if user.username == username and user.password == password), None)
    
    if user:
        session['username'] = username
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8151, debug=True)
