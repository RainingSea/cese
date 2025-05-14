from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

class FeedbackManager:
    def __init__(self, feedback_file='feedback.txt', categories_file='categories.txt'):
        self.feedback_file = feedback_file
        self.categories_file = categories_file
        if not os.path.exists(self.feedback_file):
            open(self.feedback_file, 'w').close()
        if not os.path.exists(self.categories_file):
            with open(self.categories_file, 'w') as f:
                f.write("General\nTechnical\nHR\nOther\n")

    def submit_feedback(self, username, category, content):
        feedback_id = str(int(datetime.now().timestamp()))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.feedback_file, 'a') as f:
            f.write(f"{feedback_id}|{username}|{category}|{content}|Submitted|{timestamp}\n")
        return True

    def get_user_feedback(self, username):
        feedbacks = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[1] == username:
                    feedbacks.append({
                        'id': parts[0],
                        'category': parts[2],
                        'content': parts[3],
                        'status': parts[4],
                        'timestamp': parts[5]
                    })
        return feedbacks

    def get_all_feedback(self):
        feedbacks = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                feedbacks.append({
                    'id': parts[0],
                    'username': parts[1],
                    'category': parts[2],
                    'content': parts[3],
                    'status': parts[4],
                    'timestamp': parts[5]
                })
        return feedbacks

    def update_status(self, feedback_id, status):
        lines = []
        updated = False
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == feedback_id:
                    parts[4] = status
                    line = '|'.join(parts) + '\n'
                    updated = True
                lines.append(line)
        
        if updated:
            with open(self.feedback_file, 'w') as f:
                f.writelines(lines)
            return True
        return False

    def get_categories(self):
        with open(self.categories_file, 'r') as f:
            return [line.strip() for line in f]

user_manager = UserManager()
feedback_manager = FeedbackManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    is_manager = username.startswith('manager_')
    
    if is_manager:
        feedbacks = feedback_manager.get_all_feedback()
        return render_template('dashboard.html', is_manager=True, feedbacks=feedbacks)
    else:
        feedbacks = feedback_manager.get_user_feedback(username)
        categories = feedback_manager.get_categories()
        return render_template('dashboard.html', is_manager=False, feedbacks=feedbacks, categories=categories)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    category = request.form['category']
    content = request.form['content']
    feedback_manager.submit_feedback(username, category, content)
    return redirect(url_for('dashboard'))

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session or not session['username'].startswith('manager_'):
        return redirect(url_for('login'))
    
    feedback_id = request.form['feedback_id']
    status = request.form['status']
    feedback_manager.update_status(feedback_id, status)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8100, debug=False)
