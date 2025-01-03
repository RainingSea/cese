from flask import Flask, render_template, request, redirect, session
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    current_index = session.get('current_index', 0)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'previous':
            current_index = max(0, current_index - 1)
        elif action == 'next':
            current_index = min(len(tip_manager.get_all_tips()) - 1, current_index + 1)
        session['current_index'] = current_index

    current_tip = tip_manager.get_current_tip()
    return render_template('tips.html', tip=current_tip, current_index=current_index)

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    all_tips = tip_manager.get_all_tips()
    search_query = request.form.get('search_query', '')
    if search_query:
        all_tips = tip_manager.search_tips(search_query)
    return render_template('archive.html', tips=all_tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/feedback')
    all_feedback = feedback_manager.get_all_feedback()
    return render_template('feedback.html', feedback=all_feedback)

if __name__ == '__main__':
    app.run(port=8124, debug=True)
