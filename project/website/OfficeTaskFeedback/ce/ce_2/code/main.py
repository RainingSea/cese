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
def feedback_submission():
    if request.method == 'POST':
        username = session.get('username')
        feedback = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback, category)
        return redirect(url_for('feedback_review'))
    return render_template('feedback_submission.html')

@app.route('/feedback_review')
def feedback_review():
    feedbacks = feedback_manager.get_feedbacks()
    return render_template('feedback_review.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=8364, debug=False)
