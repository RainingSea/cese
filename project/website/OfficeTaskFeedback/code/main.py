from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import fcntl
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                f.write('admin|admin123|1\n')

    def username_exists(self, username):
        with open(self.users_file, 'r') as f:
            for line in f:
                existing_user = line.strip().split('|')[0]
                if existing_user == username:
                    return True
        return False

    def register(self, username, password, is_manager):
        if self.username_exists(username):
            return False
            
        try:
            with open(self.users_file, 'a') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(f"{username}|{password}|{1 if is_manager else 0}\n")
                return True
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

    def validate_login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def is_manager(self, username):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3 and parts[0] == username:
                    return parts[2] == '1'
        return False

class FeedbackTracker:
    def __init__(self, feedback_file='feedback.txt', categories_file='categories.txt'):
        self.feedback_file = feedback_file
        self.categories_file = categories_file
        
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                pass
                
        if not os.path.exists(self.categories_file):
            with open(self.categories_file, 'w') as f:
                f.write("Task Clarity\nResources\nDeadlines\nOther")

    def get_categories(self):
        with open(self.categories_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def submit_feedback(self, username, category, content):
        if not content.strip() or category not in self.get_categories():
            return False
            
        try:
            with open(self.feedback_file, 'a+') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.seek(0)
                lines = f.readlines()
                last_id = int(lines[-1].split('|')[0]) if lines else 0
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{last_id + 1}|{username}|{timestamp}|{category}|{content}|Pending\n")
                return True
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

    def get_user_feedback(self, username):
        feedback = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6 and parts[1] == username:
                    feedback.append({
                        'id': parts[0],
                        'timestamp': parts[2],
                        'category': parts[3],
                        'content': parts[4],
                        'status': parts[5]
                    })
        return feedback

    def get_all_feedback(self, status_filter=None):
        feedback = []
        with open(self.feedback_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    if not status_filter or parts[5] == status_filter:
                        feedback.append({
                            'id': parts[0],
                            'username': parts[1],
                            'timestamp': parts[2],
                            'category': parts[3],
                            'content': parts[4],
                            'status': parts[5]
                        })
        return feedback

    def update_status(self, feedback_id, status):
        if status not in ['Pending', 'Reviewed', 'Resolved']:
            return False
            
        try:
            with open(self.feedback_file, 'r+') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                lines = f.readlines()
                updated = False
                
                for i, line in enumerate(lines):
                    parts = line.strip().split('|')
                    if len(parts) == 6 and parts[0] == feedback_id:
                        lines[i] = f"{parts[0]}|{parts[1]}|{parts[2]}|{parts[3]}|{parts[4]}|{status}\n"
                        updated = True
                
                if updated:
                    f.seek(0)
                    f.writelines(lines)
                    f.truncate()
                    return True
                return False
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

user_manager = UserManager()
feedback_tracker = FeedbackTracker()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required', 'danger')
        elif user_manager.validate_login(username, password):
            session['username'] = username
            session['is_manager'] = user_manager.is_manager(username)
            return redirect(url_for('manager_dashboard' if session['is_manager'] else 'employee_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        is_manager = 'is_manager' in request.form
        
        if not username or not password:
            flash('Username and password are required', 'danger')
        elif user_manager.username_exists(username):
            flash('Username already exists', 'danger')
        elif user_manager.register(username, password, is_manager):
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed', 'danger')
    return render_template('register.html')

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' not in session or session.get('is_manager'):
        return redirect(url_for('login'))
    
    feedback = feedback_tracker.get_user_feedback(session['username'])
    return render_template('employee_dashboard.html', 
                         username=session['username'], 
                         feedback=feedback,
                         categories=feedback_tracker.get_categories())

@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' not in session or not session.get('is_manager'):
        return redirect(url_for('login'))
    
    status_filter = request.args.get('status')
    feedback = feedback_tracker.get_all_feedback(status_filter)
    return render_template('manager_dashboard.html', 
                         username=session['username'], 
                         feedback=feedback,
                         status_filter=status_filter)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' not in session or session.get('is_manager'):
        return redirect(url_for('login'))
    
    category = request.form.get('category', '').strip()
    content = request.form.get('content', '').strip()
    
    if not category or not content:
        flash('Category and content are required', 'danger')
    elif feedback_tracker.submit_feedback(session['username'], category, content):
        flash('Feedback submitted successfully', 'success')
    else:
        flash('Failed to submit feedback', 'danger')
    
    return redirect(url_for('employee_dashboard'))

@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session or not session.get('is_manager'):
        return redirect(url_for('login'))
    
    feedback_id = request.form.get('feedback_id', '').strip()
    status = request.form.get('status', '').strip()
    
    if not feedback_id or not status:
        flash('Invalid request', 'danger')
    elif feedback_tracker.update_status(feedback_id, status):
        flash('Status updated successfully', 'success')
    else:
        flash('Failed to update status', 'danger')
    
    return redirect(url_for('manager_dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_manager', None)
    response = redirect(url_for('login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    flash('You have been logged out', 'info')
    return response

if __name__ == '__main__':
    app.run(port=8104, debug=False)
