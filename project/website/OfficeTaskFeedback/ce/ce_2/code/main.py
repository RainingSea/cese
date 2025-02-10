from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
user_manager = UserManager('users.txt')
feedback_manager = FeedbackManager('feedback.txt', 'status.txt')

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

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('feedback'))
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(session['username'], feedback_text, category)
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    feedback_list = feedback_manager.load_feedback()
    return render_template('status.html', feedbacks=feedback_list)

if __name__ == '__main__':
    app.run(port=8659, debug=False)
