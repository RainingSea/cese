from flask import Flask, render_template, request, redirect, session, url_for
from user_manager import UserManager
from tip_manager import TipManager
from feedback_manager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Initialize managers
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

@app.route('/tips', methods=['GET'])
def tips():
    current_tip = tip_manager.get_current_tip()
    current_index = 0  # Assuming the first tip is the current one
    return render_template('tips.html', tip=current_tip, current_index=current_index)

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    if request.method == 'POST':
        query = request.form['query']
        tips = tip_manager.search_tips(query)
    else:
        tips = tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect(url_for('feedback'))
    all_feedback = feedback_manager.get_all_feedback()
    return render_template('feedback.html', feedback=all_feedback)

if __name__ == '__main__':
    app.run(port=8123, debug=True)
