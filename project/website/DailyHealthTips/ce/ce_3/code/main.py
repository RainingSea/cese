from flask import Flask, render_template, request, redirect, session
from user import User
from daily_tip import DailyTip
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

def load_daily_tips():
    tips = []
    with open('daily_tips.txt', 'r') as f:
        for line in f:
            tip, date = line.strip().split('|')
            tips.append(DailyTip(tip, date))
    return tips

def load_feedback():
    feedbacks = []
    with open('feedback.txt', 'r') as f:
        for line in f:
            username, comment = line.strip().split('|')
            feedbacks.append(Feedback(username, comment))
    return feedbacks

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/tips')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/tips')
def tips():
    daily_tips = load_daily_tips()
    return render_template('tips.html', tips=daily_tips)

@app.route('/archive')
def archive():
    daily_tips = load_daily_tips()
    return render_template('archive.html', tips=daily_tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = session.get('username')
        comment = request.form['comment']
        new_feedback = Feedback(username, comment)
        new_feedback.save()
        return redirect('/tips')
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8620, debug=False)
