from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [{'username': line.split('|')[0], 'password': line.split('|')[1].strip()} for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

class FeedbackManager:
    def __init__(self):
        self.feedbacks = []
        self.load_feedback()

    def submit_feedback(self, username: str, feedback: str, category: str) -> bool:
        self.feedbacks.append({'username': username, 'feedback': feedback, 'category': category, 'status': 'Pending'})
        self.save_feedback()
        return True

    def load_feedback(self) -> None:
        if os.path.exists('feedback.json'):
            with open('feedback.json', 'r') as file:
                self.feedbacks = [json.loads(line.strip()) for line in file.readlines()]

    def save_feedback(self) -> None:
        with open('feedback.json', 'w') as file:
            for feedback in self.feedbacks:
                file.write(json.dumps(feedback) + '\n')

    def get_feedback_status(self, username: str) -> list:
        return [feedback for feedback in self.feedbacks if feedback['username'] == username]

user_manager = UserManager()
feedback_manager = FeedbackManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('feedback'))
    else:
        flash('Invalid username or password!')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!')
    return render_template('registration.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        username = session.get('username')
        feedback_text = request.form['feedback']
        category = request.form['category']
        feedback_manager.submit_feedback(username, feedback_text, category)
        flash('Feedback submitted successfully!')
        return redirect(url_for('status'))
    return render_template('feedback.html')

@app.route('/status')
def status():
    username = session.get('username')
    feedback_status = feedback_manager.get_feedback_status(username)
    return render_template('status.html', feedbacks=feedback_status)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8201, debug=False)
