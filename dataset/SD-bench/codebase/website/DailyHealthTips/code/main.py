from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users
def load_users():
    return User.load_all()

# Load tips
def load_tips():
    return Tip.load_all()

# Load feedback
def load_feedback():
    return Feedback.load_all()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tips')
def tips():
    tips = load_tips()
    return render_template('tips.html', tips=tips)

@app.route('/archive')
def archive():
    tips = load_tips()
    return render_template('archive.html', tips=tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        feedback = Feedback(username, message)
        feedback.save()
        return redirect(url_for('login'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8318, debug=False)
