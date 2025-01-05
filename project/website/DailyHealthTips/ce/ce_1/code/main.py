from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt')
feedback_manager = FeedbackManager('feedback.txt')

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
    return render_template('register.html')

@app.route('/tips')
def tips():
    current_tip_index = request.args.get('index', 0, type=int)
    tip = tip_manager.get_daily_tip()
    return render_template('tips.html', tip=tip, current_index=current_tip_index)

@app.route('/archive')
def archive():
    tips_list = tip_manager.load_tips()
    return render_template('archive.html', tips_list=tips_list)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect(url_for('tips'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8015, debug=False)
