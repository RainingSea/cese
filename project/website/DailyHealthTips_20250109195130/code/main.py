from flask import Flask, render_template, request, redirect, session
from user import User
from tip import Tip
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users() -> list:
    """Load users from the users.txt file."""
    return User.load_all()

def load_tips() -> list:
    """Load tips from the tips.txt file."""
    return Tip.load_all()

def load_feedback() -> list:
    """Load feedback from the feedback.txt file."""
    feedbacks = []
    with open('feedback.txt', 'r') as file:
        for line in file:
            username, message = line.strip().split('|')
            feedbacks.append(Feedback(username, message))
    return feedbacks

def search_tips(query: str) -> list:
    """Search for tips containing the query."""
    tips = load_tips()
    return [tip for tip in tips if query.lower() in tip.content.lower()]

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect('/tips')
        return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if any(user.username == username for user in users):
            return render_template('register.html', error="Username already exists.")
        new_user = User(username, password)
        new_user.save()
        return redirect('/')
    return render_template('register.html')

@app.route('/tips', methods=['GET', 'POST'])
def tips():
    """Display daily health tips and handle search functionality."""
    daily_tips = load_tips()
    search_results = []
    if request.method == 'POST':
        query = request.form['search']
        search_results = search_tips(query)
    return render_template('tips.html', tips=search_results or daily_tips)

@app.route('/archive')
def archive():
    """Display all tips in the archive."""
    all_tips = load_tips()
    return render_template('archive.html', tips=all_tips)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """Handle user feedback submission."""
    if request.method == 'POST':
        username = session.get('username')
        message = request.form['message']
        new_feedback = Feedback(username, message)
        new_feedback.save()
        return redirect('/feedback')
    return render_template('feedback.html', feedbacks=load_feedback())

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8357, debug=False)
