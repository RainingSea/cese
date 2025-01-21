from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
            return redirect('/')
    return render_template('register.html')

@app.route('/tip')
def tip():
    current_tip = tip_manager.get_current_tip()
    return render_template('tip.html', tip=current_tip)

@app.route('/archive')
def archive():
    tips = tip_manager.tips
    return render_template('archive.html', tips=tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/feedback')
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=9024, debug=False)
