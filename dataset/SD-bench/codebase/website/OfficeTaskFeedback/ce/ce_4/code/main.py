from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from feedback import Feedback
from feedback_tracker import FeedbackTracker

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a random secret key in production
tracker = FeedbackTracker()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register_user(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if tracker.login_user(username, password):
        session['username'] = username
        return redirect(url_for('feedback'))
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        content = request.form['content']
        category = request.form['category']
        tracker.submit_feedback(session['username'], content, category)
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    feedback_status = tracker.get_feedback_status(session['username'])
    return render_template('status.html', feedback_status=feedback_status)

if __name__ == '__main__':
    app.run(port=8661, debug=False)
