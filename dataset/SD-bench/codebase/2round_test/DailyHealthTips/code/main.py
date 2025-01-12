from flask import Flask, render_template, request, redirect, url_for, session
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

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('tips'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_tip_index = int(request.args.get('index', 0))
    current_tip = tip_manager.get_tip(current_tip_index)
    return render_template('tips.html', tip=current_tip, index=current_tip_index)

@app.route('/archive')
def archive():
    if 'username' not in session:
        return redirect(url_for('login'))
    all_tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=all_tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect(url_for('tips'))
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/next_tip')
def next_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_index = int(request.args.get('index', 0))
    return redirect(url_for('tips', index=current_index + 1))

@app.route('/previous_tip')
def previous_tip():
    if 'username' not in session:
        return redirect(url_for('login'))
    current_index = int(request.args.get('index', 0))
    return redirect(url_for('tips', index=current_index - 1))

if __name__ == '__main__':
    app.run(port=8066, debug=False)
