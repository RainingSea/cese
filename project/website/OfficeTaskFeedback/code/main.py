from flask import Flask, render_template, request, redirect, url_for, session, flash
from UserManager import UserManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user_manager.register(username, password)
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except ValueError as e:
            flash(str(e))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('feedback_submission'))
    flash('Login failed. Please check your username and password.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_submission():
    """Handle feedback submission."""
    if request.method == 'POST':
        feedback = request.form['feedback']
        category = request.form['category']
        username = session.get('username')
        try:
            feedback_manager.submit(feedback, category, username)
            flash('Feedback submitted successfully!')
            return redirect(url_for('feedback_review'))
        except ValueError as e:
            flash(str(e))
    return render_template('feedback_submission.html')

@app.route('/feedback/review')
def feedback_review():
    """Render feedback review page for managers."""
    if 'username' in session and user_manager.is_manager(session['username']):
        feedbacks = feedback_manager.get_feedbacks()
        return render_template('feedback_review.html', feedback=feedbacks)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8479, debug=False)
