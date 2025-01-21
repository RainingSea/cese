from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from TipManager import TipManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

user_manager = UserManager()
tip_manager = TipManager()
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
            return redirect('/')
    return render_template('register.html')

@app.route('/tips')
def tips():
    current_tip = tip_manager.get_current_tip()
    return render_template('tips.html', tip=current_tip)

@app.route('/archive')
def archive():
    return render_template('archive.html', tips=tip_manager.tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        user = session.get('username', 'Guest')
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(user, feedback_text)
        return redirect('/tips')
    return render_template('feedback.html')

if __name__ == '__main__':
    user_manager.load_users()
    tip_manager.load_tips()
    feedback_manager.load_feedback()
    app.run(port=9026, debug=False)
