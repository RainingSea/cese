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

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['user_id'] = username
        return redirect(url_for('feedback'))
    flash("Invalid username or password.")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
        flash("Registration failed. Username already exists.")
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')
        category = request.form['category']
        content = request.form['content']
        feedback_manager.submit_feedback(user_id, category, content)
        return redirect(url_for('feedback_status'))
    return render_template('feedback.html')

@app.route('/review')
def review():
    feedbacks = feedback_manager.review_feedback()
    return render_template('review.html', feedbacks=feedbacks)

@app.route('/feedback_status')
def feedback_status():
    user_id = session.get('user_id')
    status = feedback_manager.get_feedback_status(user_id)
    return render_template('status.html', status=status)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8477, debug=False)
