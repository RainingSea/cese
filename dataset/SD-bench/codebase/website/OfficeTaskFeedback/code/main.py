from flask import Flask, render_template, request, redirect, session
from user import User
from feedback import Feedback
from feedback_tracker import FeedbackTracker

app = Flask(__name__)
app.secret_key = 'your_secret_key'
tracker = FeedbackTracker()

def load_users() -> list:
    """Load users from the users.txt file."""
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

users = load_users()

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect('/feedback')
    return render_template('login.html')

def login_user(username: str, password: str) -> bool:
    """Check if the user can log in with the provided credentials."""
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect('/')
    return render_template('register.html')

def register_user(username: str, password: str) -> bool:
    """Register a new user if the username is not taken."""
    if any(user.username == username for user in users):
        return False
    new_user = User(username, password)
    new_user.save()
    users.append(new_user)
    return True

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Handle feedback submission."""
    if 'username' not in session:
        return redirect('/')  # Ensure user is logged in
    if request.method == 'POST':
        user = session['username']
        content = request.form['content']
        category = request.form['category']
        submit_feedback(user, content, category)
        return redirect('/status')
    return render_template('feedback.html')

def submit_feedback(user: str, content: str, category: str) -> None:
    """Submit feedback from the user."""
    feedback = Feedback(user, content, category)
    feedback.save()
    tracker.track_feedback(feedback)

@app.route('/status')
def status():
    """Display the status of the user's feedback."""
    user = session.get('username')
    if user is None:
        return redirect('/')  # Ensure user is logged in
    feedback_status = tracker.get_status(user)
    return render_template('status.html', feedback_status=feedback_status)

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8662, debug=False)
