from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
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
            return redirect(url_for('archive'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/archive')
def archive():
    if 'username' not in session:
        return redirect(url_for('login'))
    daily_tip = tip_manager.get_daily_tip()
    return render_template('archive.html', username=session['username'], daily_tip=daily_tip)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_feedback = request.form['feedback']
        feedback_manager.submit_feedback(session['username'], user_feedback)
        return redirect(url_for('archive'))
    return render_template('feedback.html', username=session['username'])

@app.route('/tips')
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    all_tips = tip_manager.get_all_tips()
    return render_template('archive.html', username=session['username'], all_tips=all_tips)

if __name__ == '__main__':
    app.run(debug=True)