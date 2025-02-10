from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

# Load users
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

# Load tips
def load_tips():
    tips = []
    with open('tips.txt', 'r') as file:
        for line in file:
            content, date = line.strip().split('|')
            tips.append(Tip(content, date))
    return tips

# Load feedback
def load_feedback():
    feedback_list = []
    with open('feedback.txt', 'r') as file:
        for line in file:
            username, message = line.strip().split('|')
            feedback_list.append(Feedback(username, message))
    return feedback_list

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tip')
def daily_tip():
    tips = load_tips()
    return render_template('tip.html', tip=tips[-1])  # Display the latest tip

@app.route('/archive')
def archive():
    tips = load_tips()
    return render_template('archive.html', tips=tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        new_feedback = Feedback(username, message)
        new_feedback.save()
        return redirect(url_for('feedback'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8621, debug=False)
