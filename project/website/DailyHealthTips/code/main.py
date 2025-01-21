from flask import Flask, render_template, request, redirect, session
from UserManager import UserManager
from TipManager import TipManager
from FeedbackManager import FeedbackManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
tip_manager = TipManager('tips.txt')
feedback_manager = FeedbackManager('feedback.txt')

@app.route('/')
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    """Handles user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        session['current_tip_index'] = 0  # Initialize tip index on login
        return redirect('/tips')
    return render_template('login.html', error="Invalid credentials.")

@app.route('/logout')
def logout():
    """Handles user logout."""
    user_manager.logout(session)
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.is_username_taken(username):
            return render_template('register.html', error="Username already taken.")
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    """Displays tips and handles navigation between them."""
    current_index = session.get('current_tip_index', 0)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'next':
            current_index += 1
        elif action == 'previous':
            current_index -= 1
        session['current_tip_index'] = current_index

    current_tip = tip_manager.get_current_tip(current_index)
    return render_template('tips.html', tip=current_tip)

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    """Displays the tips archive and handles search functionality."""
    search_query = request.form.get('search', '')
    tips = tip_manager.search_tips(search_query) if search_query else tip_manager.get_all_tips()
    return render_template('archive.html', tips=tips, search_query=search_query)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Handles feedback submission and displays previous feedback."""
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        feedback_manager.submit_feedback(feedback_text)
        return redirect('/feedback')
    return render_template('feedback.html', feedbacks=feedback_manager.feedback_list)

if __name__ == '__main__':
    app.run(port=9027, debug=False)
