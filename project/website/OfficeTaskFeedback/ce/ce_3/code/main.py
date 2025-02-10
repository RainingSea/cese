from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from feedback import Feedback
from feedback_tracker import FeedbackTracker

app = Flask(__name__)
app.secret_key = 'your_secret_key'
tracker = FeedbackTracker('users.txt', 'feedback.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        content = request.form['content']
        category = request.form['category']
        user = session.get('username')
        tracker.submit_feedback(user, content, category)
        return redirect(url_for('dashboard'))
    return render_template('feedback.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('username')
    feedback_list = tracker.get_feedback(user) if user else []
    return render_template('dashboard.html', feedbacks=feedback_list)

if __name__ == '__main__':
    app.run(port=8660, debug=False)
