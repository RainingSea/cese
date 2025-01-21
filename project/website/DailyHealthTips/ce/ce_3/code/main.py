from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from TipManager import TipManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
            return redirect('/main')
    return render_template('login.html')

@app.route('/main')
def main():
    current_tip = tip_manager.get_current_tip()
    return render_template('main.html', tip=current_tip)

@app.route('/archive')
def archive():
    tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/main')
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=9025, debug=False)
