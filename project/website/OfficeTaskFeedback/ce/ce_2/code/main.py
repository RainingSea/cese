from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime

class FeedbackTracker:
    def __init__(self, users_file='users.txt', feedback_file='feedback.txt'):
        self.users_file = users_file
        self.feedback_file = feedback_file
        if not os.path.exists(users_file):
            open(users_file, 'w').close()
        if not os.path.exists(feedback_file):
            open(feedback_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.strip():
                    existing_user, _ = line.strip().split('|')
                    if existing_user == username:
                        return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.strip():
                    user, pwd = line.strip().split('|')
                    if user == username and pwd == password:
                        return True
        return False

    def submit_feedback(self, username, task, feedback, category):
        feedback_id = str(len(open(self.feedback_file).readlines()) + 1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'id': feedback_id,
            'username': username,
            'task': task,
            'feedback': feedback,
            'category': category,
            'status': 'Pending',
            'timestamp': timestamp
        }
        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        return True

    def get_feedback(self, username, is_manager=False):
        feedback = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line.strip())
                    if is_manager or entry['username'] == username:
                        feedback.append(entry)
        return feedback

    def update_feedback_status(self, feedback_id, status):
        entries = []
        updated = False
        with open(self.feedback_file, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line.strip())
                    if entry['id'] == feedback_id:
                        entry['status'] = status
                        updated = True
                    entries.append(entry)
        
        if updated:
            with open(self.feedback_file, 'w') as f:
                for entry in entries:
                    f.write(json.dumps(entry) + '\n')
        return updated

app = Flask(__name__)
app.secret_key = 'secret_key'
tracker = FeedbackTracker()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if tracker.login(username, password):
            session['username'] = username
            session['is_manager'] = (username == 'admin')
            return redirect(url_for('manager_dashboard' if session['is_manager'] else 'employee_dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('register.html', error="Passwords don't match")
        if tracker.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        task = request.form['task']
        feedback_text = request.form['feedback']
        category = request.form['category']
        tracker.submit_feedback(session['username'], task, feedback_text, category)
        return redirect(url_for('employee_dashboard'))
    
    return render_template('feedback.html')

@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' not in session or not session['is_manager']:
        return redirect(url_for('login'))
    
    feedback = tracker.get_feedback(session['username'], is_manager=True)
    category_filter = request.args.get('category')
    if category_filter:
        feedback = [f for f in feedback if f['category'] == category_filter]
    
    return render_template('manager_dashboard.html', feedback=feedback)

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    feedback = tracker.get_feedback(session['username'])
    return render_template('employee_dashboard.html', feedback=feedback)

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session or not session['is_manager']:
        return redirect(url_for('login'))
    
    feedback_id = request.form['feedback_id']
    status = request.form['status']
    tracker.update_feedback_status(feedback_id, status)
    return redirect(url_for('manager_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8102, debug=False)
