from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('tips'))
        return render_template('login.html', error='Invalid credentials.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Registration failed.')
    return render_template('register.html')

@app.route('/tips', methods=['GET'])
def tips():
    current_tip = tip_manager.get_current_tip()
    return render_template('tips.html', tip=current_tip)

@app.route('/feedback', methods=['POST'])
def feedback():
    user = session.get('username', 'Guest')
    feedback_text = request.form['feedback']
    feedback_manager.submit_feedback(user, feedback_text)
    return redirect(url_for('tips'))

if __name__ == '__main__':
    app.run(port=8317, debug=False)
