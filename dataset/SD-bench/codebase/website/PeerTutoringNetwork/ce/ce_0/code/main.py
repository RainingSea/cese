from flask import Flask, render_template, request, redirect, url_for, session
from FileManager import FileManager
from User import User
from Tutor import Tutor
from TutoringRequest import TutoringRequest
from SupportContact import SupportContact

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
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
        user = User(username, password, email)
        file_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    tutors = file_manager.load_tutors()
    return render_template('dashboard.html', tutors=tutors)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact = SupportContact(name, email, message)
        file_manager.save_contact(contact)
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/request_tutoring', methods=['GET', 'POST'])
def request_tutoring():
    if request.method == 'POST':
        username = request.form['username']
        subject = request.form['subject']
        details = request.form['details']
        preferred_date = request.form['preferred_date']
        request = TutoringRequest(username, subject, details, preferred_date)
        file_manager.save_request(request)
        return redirect(url_for('dashboard'))
    return render_template('request_tutoring.html')

if __name__ == '__main__':
    app.run(port=8675, debug=False)
