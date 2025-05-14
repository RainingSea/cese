from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'  # Required for session management

class FeedbackTracker:
    def __init__(self):
        self.users_file = 'users.txt'
        self.feedback_file = 'feedback.txt'
        self.categories_file = 'categories.txt'
        self.ensure_files_exist()

    def ensure_files_exist(self):
        for filename in [self.users_file, self.feedback_file, self.categories_file]:
            if not os.path.exists(filename):
                open(filename, 'a').close()

    def register_user(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.split('|')[0] == username:
                    return False
            f.write(f"{username}|{password}\n")
        return True

    def authenticate(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def submit_feedback(self, username, category, content):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.feedback_file, 'a') as f:
            f.write(f"{username}|{timestamp}|{category}|{content}|pending\n")
        return True

    def get_feedback(self, for_manager=False, username=None):
        feedback = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    if for_manager or (username and parts[0] == username):
                        feedback.append({
                            'username': parts[0],
                            'timestamp': parts[1],
                            'category': parts[2],
                            'content': parts[3],
                            'status': parts[4]
                        })
        return feedback

    def update_status(self, feedback_id, new_status):
        feedback_id = int(feedback_id)
        with open(self.feedback_file, 'r') as f:
            lines = f.readlines()
        
        if feedback_id < 0 or feedback_id >= len(lines):
            return False
        
        parts = lines[feedback_id].strip().split('|')
        if len(parts) == 5:
            lines[feedback_id] = f"{parts[0]}|{parts[1]}|{parts[2]}|{parts[3]}|{new_status}\n"
        
        with open(self.feedback_file, 'w') as f:
            f.writelines(lines)
        return True

    def get_categories(self):
        with open(self.categories_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]

tracker = FeedbackTracker()

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
        if tracker.authenticate(username, password):
            session['username'] = username
            session['is_manager'] = username == 'manager'  # Simple manager check
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.register_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    is_manager = session.get('is_manager', False)
    
    if is_manager:
        feedback = tracker.get_feedback(for_manager=True)
    else:
        feedback = tracker.get_feedback(username=username)
    
    categories = tracker.get_categories()
    return render_template('dashboard.html', 
                         username=username,
                         is_manager=is_manager,
                         feedback=feedback,
                         categories=categories)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    category = request.form['category']
    content = request.form['content']
    
    tracker.submit_feedback(username, category, content)
    return redirect(url_for('dashboard'))

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session or not session.get('is_manager', False):
        return redirect(url_for('login'))
    
    feedback_id = request.form['feedback_id']
    new_status = request.form['status']
    
    tracker.update_status(feedback_id, new_status)
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8098, debug=False)
