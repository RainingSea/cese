from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from feedback_manager import FeedbackManager

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
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = session['username']
        feedback_text = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback_text, category)
        return redirect(url_for('feedback'))
    return render_template('feedback_submission.html')

@app.route('/review')
def review():
    feedbacks = feedback_manager.review_feedback()
    return render_template('feedback_review.html', feedbacks=feedbacks)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('feedback'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8362, debug=False)
