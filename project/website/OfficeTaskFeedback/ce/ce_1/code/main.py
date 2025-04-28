from flask import Flask, render_template, request, redirect, url_for, flash
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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.')
    return render_template('registration.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = request.form['username']
        category = request.form['category']
        feedback_text = request.form['feedback']
        if feedback_manager.submit_feedback(username, category, feedback_text):
            flash('Feedback submitted successfully!')
            return redirect(url_for('feedback'))
        else:
            flash('Failed to submit feedback.')
    return render_template('feedback.html')

@app.route('/review')
def review():
    feedbacks = feedback_manager.get_feedbacks()
    return render_template('review.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(port=8363, debug=False)
