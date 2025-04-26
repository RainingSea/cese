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
        user = session.get('username')
        feedback_text = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(user, feedback_text, category)
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    user = session.get('username')
    feedback_status = feedback_manager.get_feedback_status(user)
    return render_template('status.html', feedback_status=feedback_status)

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('feedback'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8199, debug=False)
