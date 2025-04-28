from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
tip_manager = TipManager('health_tips.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/tips')
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
        else:
            return "Registration failed, username may already exist."
    return render_template('register.html')

@app.route('/tips')
def tips():
    current_tip = tip_manager.get_current_tip()
    return render_template('tips.html', tip=current_tip)

@app.route('/archive')
def archive():
    tips_list = tip_manager.search_tips('')
    return render_template('archive.html', tips=tips_list)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/tips')
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(port=8315, debug=False)
