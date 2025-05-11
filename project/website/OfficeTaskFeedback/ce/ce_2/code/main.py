from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
feedback_manager = FeedbackManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username already exists.', 'error')
    return render_template('registration.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if 'username' in session:
        if request.method == 'POST':
            feedback = request.form['feedback']
            category = request.form['category']
            feedback_manager.submit_feedback(session['username'], feedback, category)
            return redirect(url_for('status_display'))
        return render_template('feedback_submission.html')
    return redirect(url_for('login'))

@app.route('/feedback_review')
def feedback_review():
    if 'username' in session and user_manager.is_manager(session['username']):
        feedbacks = feedback_manager.get_feedbacks()
        return render_template('feedback_review.html', feedbacks=feedbacks)
    return redirect(url_for('login'))

@app.route('/status_display')
def status_display():
    if 'username' in session:
        statuses = feedback_manager.get_feedback_status(session['username'])
        return render_template('status_display.html', statuses=statuses)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('submit_feedback'))
    flash('Login failed. Please check your username and password.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8478, debug=False)
