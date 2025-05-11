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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username already exists.')
    return render_template('registration.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')
        content = request.form['content']
        category = request.form['category']
        feedback_manager.submit_feedback(user_id, content, category)
        return redirect(url_for('status'))
    return render_template('feedback_submission.html')

@app.route('/feedback_review')
def feedback_review():
    feedbacks = feedback_manager.review_feedback()
    return render_template('feedback_review.html', feedbacks=feedbacks)

@app.route('/status')
def status():
    user_id = session.get('user_id')
    feedback_status = feedback_manager.get_feedback_status(user_id)
    return render_template('status.html', feedback_status=feedback_status)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['user_id'] = username
        return redirect(url_for('status'))
    flash('Login failed. Please check your username and password.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8476, debug=False)
