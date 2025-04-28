from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from UserManager import UserManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'supersecretkey'  # Required for flash messages
Session(app)

user_manager = UserManager('users.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    return render_template('registration.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        username = session.get('username')
        feedback = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback, category)
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    username = session.get('username')
    feedback_status = feedback_manager.get_feedback_status(username)
    return render_template('status.html', feedback_status=feedback_status)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        flash('Login successful!', 'success')
        return redirect(url_for('submit_feedback'))
    flash('Invalid username or password. Please try again.', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8365, debug=False)
